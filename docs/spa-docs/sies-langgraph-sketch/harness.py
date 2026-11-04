#!/usr/bin/env python3
"""
Reference Gate 3 harness (stub).

Produces the receipts defined in GATE-3-HARNESS.md.
Run from the sies-langgraph-sketch directory after the sies package is on the path.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

# Assumes sketch.py classes are importable or duplicated minimally
# For a real drop-in, import from sketch import ContentAddressedNode, DeterministicSettler, sha256_hex
# Here we show the metrics and Gate3Evidence shape only.

def emit_gate3_evidence(claim_id: str, num_nodes: int, settlement: dict, wall_ms: float, provisional=None) -> dict:
    explicit_pass = settlement["payload"]["explicit_pass"]
    explicit_fail = settlement["payload"]["explicit_fail"]
    total = settlement["payload"]["total_observations"]
    evidence = {
        "claim_id": claim_id,
        "num_nodes": num_nodes,
        "explicit_pass": explicit_pass,
        "explicit_fail": explicit_fail,
        "explicit_yield": (explicit_pass + explicit_fail) / total if total else 0.0,
        "settlement_state": settlement["state"],
        "provisional_direction": provisional,
        "mismatch": settlement["learning"]["mismatch"],
        "wall_time_ms": wall_ms,
        "scale_probe": False,
    }
    return evidence

def emit_metrics(evidence: dict) -> dict:
    return {
        "explicit_yield": evidence["explicit_yield"],
        "conflict_rate": 1.0 if evidence["settlement_state"] == "CONFLICT" else 0.0,
        "mismatch_rate": 1.0 if evidence["mismatch"] else 0.0,
        "hold_recommended": evidence["settlement_state"] in ("INDETERMINATE", "CONFLICT"),
        "notes": "stub harness metrics",
    }

if __name__ == "__main__":
    print("Reference harness shape only.")
    print("Integrate with sketch.ContentAddressedNode + DeterministicSettler for a full run.")
    print("See GATE-3-HARNESS.md for required receipts.")
