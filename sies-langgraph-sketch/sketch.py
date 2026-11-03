#!/usr/bin/env python3
"""
Minimal SIES + content-addressed parallel node sketch.

Maps to the graph idea:
- Nodes are content-addressed (SHA of their memory/tools contents).
- Each node runs speculatively and emits a response receipt + evidence observation.
- A deterministic settler consumes the receipts and produces a settlement receipt.
- Answer can be emitted early (confidence contract); settlement may stay INDETERMINATE or later become PASS/FAIL/CONFLICT.
- Parallel fan-out of 30–100+ stub nodes is trivial.

Run: python3 sketch.py
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import random
import time
from dataclasses import asdict
from pathlib import Path

# Import the SIES core that came with the prototype zip
from sies.core import (
    Claim,
    EvidenceObservation,
    EvidenceStatus,
    ConfidenceContract,
    SettlementPolicy,
    HeuristicPredictor,
    # The actual engine classes live in core.py; we re-use the types and logic
)
from sies.knowledge import MarkdownKnowledgeStore

# ---------------------------------------------------------------------------
# Thin wrappers so we can drive the prototype without depending on its private
# engine internals. We re-implement the minimal settlement loop using the
# public types and the invariants from the SPEC.
# ---------------------------------------------------------------------------

def sha256_hex(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


class ContentAddressedNode:
    """A graph node whose identity is the SHA of its memory + tools contents."""

    def __init__(self, node_id: str, memory_md: str, tools: dict | None = None):
        self.node_id = node_id
        self.memory_md = memory_md
        self.tools = tools or {}
        payload = json.dumps({"memory": memory_md, "tools": self.tools}, sort_keys=True)
        self.identity = sha256_hex(payload)
        self.knowledge = MarkdownKnowledgeStore()
        self.knowledge.ingest(f"nodes/{node_id}.md", memory_md)

    def execute(self, claim: Claim, seed: int | None = None) -> dict:
        """Speculative execution. Returns a response receipt + evidence observation."""
        rng = random.Random(seed or hash(self.identity + claim.claim_id) % (2**32))

        # Stub logic: most nodes return neutral or weak evidence; a few return strong.
        roll = rng.random()
        if roll < 0.05:
            status = EvidenceStatus.PASS
            weight = 1.0
            note = "strong supporting observation"
        elif roll < 0.08:
            status = EvidenceStatus.FAIL
            weight = 1.0
            note = "strong contradicting observation"
        elif roll < 0.4:
            status = EvidenceStatus.TIMEOUT
            weight = 0.0
            note = "no evidence yet"
        else:
            status = EvidenceStatus.MISSING
            weight = 0.0
            note = "deferred"

        obs = EvidenceObservation(
            evidence_id=f"ev:{self.node_id}:{claim.claim_id}",
            source=self.node_id,
            status=status,
            weight=weight,
            note=note,
        )

        # Response receipt (what the node said before settlement)
        response_payload = {
            "node_identity": self.identity,
            "claim_id": claim.claim_id,
            "observation": {
                "status": obs.status.value,
                "weight": obs.weight,
                "note": obs.note,
            },
            "ts": time.time(),
        }
        response_receipt_id = sha256_hex(json.dumps(response_payload, sort_keys=True))

        return {
            "node_id": self.node_id,
            "identity": self.identity,
            "observation": obs,
            "response_receipt_id": response_receipt_id,
            "response_payload": response_payload,
        }


class DeterministicSettler:
    """Owns the four-state settlement. Confidence never settles a claim."""

    def __init__(self, policy: SettlementPolicy | None = None):
        self.policy = policy or SettlementPolicy()
        self.predictor = HeuristicPredictor()

    def settle(self, claim: Claim, observations: list[EvidenceObservation]) -> dict:
        explicit_pass = [o for o in observations if o.status == EvidenceStatus.PASS]
        explicit_fail = [o for o in observations if o.status == EvidenceStatus.FAIL]

        if explicit_pass and explicit_fail:
            state = "CONFLICT"
        elif explicit_fail:
            state = "FAIL"
        elif explicit_pass:
            # Optional required-sources check can be added here
            state = "PASS"
        else:
            state = "INDETERMINATE"

        settlement_payload = {
            "claim_id": claim.claim_id,
            "state": state,
            "explicit_pass": len(explicit_pass),
            "explicit_fail": len(explicit_fail),
            "total_observations": len(observations),
            "ts": time.time(),
        }
        settlement_receipt_id = sha256_hex(json.dumps(settlement_payload, sort_keys=True))

        # Learning signal: provisional direction vs final settlement
        pred = self.predictor.predict(claim, observations)
        learning = {
            "provisional_direction": pred.direction.value if pred.direction else None,
            "provisional_confidence": pred.confidence,
            "final_state": state,
            "mismatch": (pred.direction.value if pred.direction else None) != state,
        }

        return {
            "settlement_receipt_id": settlement_receipt_id,
            "state": state,
            "payload": settlement_payload,
            "learning": learning,
        }


def run_parallel_experiment(num_nodes: int = 64, claim_text: str = "The far-end path is already known."):
    claim = Claim(claim_id="claim:demo:001", text=claim_text)

    # Build content-addressed nodes (stub memory)
    nodes = []
    for i in range(num_nodes):
        memory = f"# Node {i}\n\nStub memory for speculative execution.\nIdentity will be SHA of this content + tools."
        nodes.append(ContentAddressedNode(node_id=f"node-{i:04d}", memory_md=memory))

    print(f"Created {num_nodes} content-addressed nodes.")
    print(f"Sample identity: {nodes[0].identity[:20]}...")

    # Parallel speculative execution
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(32, num_nodes)) as ex:
        futures = [ex.submit(n.execute, claim) for n in nodes]
        for fut in concurrent.futures.as_completed(futures):
            results.append(fut.result())

    observations = [r["observation"] for r in results]
    settler = DeterministicSettler()
    settlement = settler.settle(claim, observations)

    # Confidence contract example (answer can be emitted early)
    contract = ConfidenceContract(min_confidence=0.7, min_explicit_observations=1)
    pred = settler.predictor.predict(claim, observations)
    answer_allowed = (
        pred.direction is not None
        and pred.confidence >= contract.min_confidence
        and sum(1 for o in observations if o.explicit) >= contract.min_explicit_observations
    )

    print("\n=== Settlement ===")
    print(f"State: {settlement['state']}")
    print(f"Explicit PASS: {settlement['payload']['explicit_pass']}")
    print(f"Explicit FAIL: {settlement['payload']['explicit_fail']}")
    print(f"Settlement receipt: {settlement['settlement_receipt_id'][:24]}...")
    print(f"Provisional answer allowed by contract: {answer_allowed} (conf={pred.confidence:.2f})")
    print(f"Learning mismatch: {settlement['learning']['mismatch']}")

    # Persist a tiny receipt log
    out = Path("receipts.jsonl")
    with out.open("w") as f:
        for r in results:
            f.write(json.dumps({
                "node_id": r["node_id"],
                "identity": r["identity"],
                "response_receipt_id": r["response_receipt_id"],
                "status": r["observation"].status.value,
            }) + "\n")
        f.write(json.dumps({"settlement": settlement["payload"], "receipt": settlement["settlement_receipt_id"]}) + "\n")
    print(f"\nWrote {out} ({num_nodes} response receipts + 1 settlement receipt)")

    return settlement


if __name__ == "__main__":
    run_parallel_experiment(num_nodes=64)
