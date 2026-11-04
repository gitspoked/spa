# EXTENSION-POINTS — Replacement Boundaries for Future Components

**Status:** Draft — informational  
**Version:** 0.1.0  
**Date:** 2026-11-03  
**Authority:** None.  
**Canonical parent:** SPEC-001

## 1. Purpose

Document the stable contracts so that stubs may be replaced without altering settlement semantics or receipt identity rules.

## 2. Node Execution Boundary

**Current:** `ContentAddressedNode.execute(claim) → {observation, response_receipt}`  
**Replaceable by:**
- LangGraph node + checkpointer
- Containerized MKZ executor (Docker or equivalent)
- Remote agent call

**Contract preserved:** ResponseReceipt + EvidenceObservation schema.

## 3. Settlement Boundary

**Current:** In-process DeterministicSettler  
**Replaceable by:** Dedicated settler service  
**Contract preserved:** SettlementReceipt schema and four-state rules. Confidence remains invisible to settler.

## 4. Receipt Persistence Boundary

**Current:** Local `receipts.jsonl`  
**Replaceable by:**
- FalkorDB property graph
- Content-addressed object store
- Git commits (each receipt a blob)
- Qdrant + metadata

**Contract preserved:** Retrievability by digest.

## 5. Memory / Identity Boundary

**Current:** Stub markdown string → SHA identity  
**Replaceable by:** Document Deterministics atomized spines (document, subject, temporal, evidence, etc.)  
**Contract preserved:** Node identity = SHA of canonical memory payload.

## 6. Predictor Boundary

**Current:** HeuristicPredictor  
**Replaceable by:** ONNX / GNN / calibrated model (see adapters.py LearnedPredictorAdapter)  
**Contract preserved:** Predictor output never written to settlement state.

## 7. Non-Replacement Items

The following are not extension points; they are invariants:
- Four-state settlement rules
- Content-addressed receipt identity
- Structure ≠ authority
- Quarantine of unresolved claims
- Amendment only via settled PASS

---

**Disposition:** Informational map for future work. No implementation required for current gates.
