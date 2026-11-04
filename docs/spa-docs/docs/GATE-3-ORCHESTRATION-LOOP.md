# GATE-3 — Minimal Orchestration Loop Specification

**Status:** Draft — Gate 3 candidate  
**Version:** 0.1.0  
**Date:** 2026-11-03  
**Authority:** None. Structure only.  
**Canonical parent:** SPEC-001  
**Related:** PROCESS.md §3, FR-003, FR-004, FR-005, FR-009, ADR-002, ADR-003

## 1. Purpose

Define the minimal executable loop that produces the evidence required for Gate 3:

> A minimal agentic loop has executed: parallel evidence collection → response receipts → deterministic settlement → (optional) LearningEvent.

The loop must be runnable with the existing `sies-langgraph-sketch` stub nodes. No production components are required.

## 2. Loop Definition

```
Claim C
  │
  ├─► [Parallel] Node_i.execute(C)  →  ResponseReceipt_i + EvidenceObservation_i
  │
  ├─► Collect observations[]
  │
  ├─► Settler.settle(C, observations)  →  SettlementReceipt
  │
  ├─► (Optional) Predictor.predict(C, observations)  →  provisional direction
  │
  └─► If provisional ≠ settlement (or unexpected gate outcome)
        LearningEvent(response, settlement)
```

All outputs are content-addressed.

## 3. Required Receipts for Gate 3

| Receipt | Required fields | Produced by |
|---------|-----------------|-------------|
| ResponseReceipt | receipt_id, claim_id, node_identity, observation status/weight/note, ts | Each node |
| SettlementReceipt | receipt_id, claim_id, state (INDETERMINATE/PASS/FAIL/CONFLICT), explicit_pass count, explicit_fail count, evidence_ids | Settler |
| LearningEvent (optional) | event_id, response_receipt_id, settlement_receipt_id, provisional_direction, provisional_confidence, settled_state, mismatch flag | Learning Agent |

## 4. Minimal Runnable Demonstration

Using the existing sketch:

```bash
cd sies-langgraph-sketch
python3 sketch.py
```

Expected output artifacts:
- Console settlement summary
- `receipts.jsonl` containing one line per node response receipt + one settlement line

This satisfies the structural evidence requirement for Gate 3 when the claim is a stub claim and nodes are stub nodes.

## 5. Evidence Checklist (Gate 3)

- [ ] At least N ≥ 30 response receipts exist (content-addressed).
- [ ] Exactly one settlement receipt exists for the claim.
- [ ] Settlement state is one of the four defined states.
- [ ] If a provisional direction was emitted, a LearningEvent exists when mismatch occurred.
- [ ] All receipts are recoverable by digest.
- [ ] No receipt is treated as approval or empirical proof.

## 6. Extension Points (not required for Gate 3)

- Replace stub `ContentAddressedNode.execute` with LangGraph node or containerized MKZ executor.
- Persist receipts to FalkorDB / object store / Git.
- Increase N to 300–1000 and observe far-end path stability.
- Feed real atomized memory (Document Deterministics spines) into node identity.

## 7. Self-Adjustment Hook

If the Gate 3 run produces a LearningEvent whose mismatch suggests the current gate criteria are insufficient or overly strict, an amendment claim may be raised. The amendment is settled independently. Prior Gate 3 definition remains addressable by digest.

---

**Disposition:** Structural specification of the minimal loop. Execution of the sketch constitutes the evidence; the evidence does not constitute approval.
