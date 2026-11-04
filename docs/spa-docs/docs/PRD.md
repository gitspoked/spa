# PRD — Product Requirements: Agentic Orchestration Layer

**Status:** Draft — Gate 1 candidate  
**Version:** 0.1.0  
**Date:** 2026-11-03  
**Authority:** None. Structure only.  
**Canonical parent:** SPEC-001

## 1. Product Summary

An evolvable agentic orchestration layer that drives the refinement and development of the receipted speculative graph system. The layer produces and gates BRD/FRD/PRD/ADR/SPEC artifacts, collects evidence in parallel, settles claims deterministically, emits learning events, and amends its own process only through settled amendments.

The product is the process, not the final graph system.

## 2. User Stories (structural)

- As a process owner, I want a single canonical SPEC so that competing definitions cannot silently diverge.
- As an orchestration agent, I want to emit a provisional direction under a confidence contract so that work can proceed while settlement remains deferred.
- As a settler, I want to consume only explicit evidence observations so that confidence never settles a claim.
- As a learning agent, I want mismatches between provisional and settled outcomes to produce LearningEvents so that the process can propose amendments.
- As an auditor, I want every significant action to carry a content-addressed receipt so that the history is reconstructible.
- As a quarantine steward, I want unresolved or competing claims isolated so that they cannot be used as premises.

## 3. Key Capabilities

1. Canonical artifact registry with digest-based identity.
2. Parallel speculative evidence collection producing response receipts.
3. Deterministic four-state settler.
4. LearningEvent generation and amendment proposal workflow.
5. Gate evaluation with explicit evidence recording.
6. Quarantine store and enforcement.
7. Recoverable history of all process versions.

## 4. Acceptance Criteria (Gate 1 — structural)

- [ ] SPEC-001, PROCESS, BRD, FRD, PRD, and at least two ADRs exist and reference one another consistently.
- [ ] All documents declare “Authority: None. Structure only.”
- [ ] Quarantine rules are stated and open questions are explicitly marked quarantined.
- [ ] Traceability from FR to SPEC/PROCESS is present.
- [ ] No document claims approval or empirical proof.

These criteria establish structural completeness only.

## 5. Future Capabilities (out of current scope)

- Integration with LangGraph checkpointers for receipt storage.
- Containerized MKZ node executors.
- Persistence to FalkorDB or equivalent property graph.
- Scaled execution (300–3000 nodes) with far-end path observation.
- Unlazy depth-tree enforcement inside orchestration loops.

## 6. Dependencies

- SIES core types (Claim, EvidenceObservation, SettlementState, receipts, LearningEvent).
- Existing sketch (`sies-langgraph-sketch/`) as the minimal executable demonstration.
- DLC Truth-Integrity Audit principles.

## 7. Risks and Mitigations

Same as BRD, plus:
- Agents treating their own outputs as settled → mitigated by mandatory settler role and receipt separation.
- Process amendment loops that never settle → mitigated by explicit quarantine of unresolved amendments.

---

**Disposition:** Draft. Completes the Gate 1 artifact set when paired with ADRs.  
**Next:** ADRs.
