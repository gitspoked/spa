# SPEC-001 — Canonical Specification: Agentic Orchestration of Receipted Speculative Graph Refinement

**Status:** Draft — Gate 0 (structure only)  
**Version:** 0.2.0 (expanded)  
**Date:** 2026-11-03  
**Authority:** None. This document defines structure. It does not constitute approval, empirical proof, or implementation authority.  
**Canonical resolution:** Single root SPEC. Competing candidates must be quarantined until explicit resolution claim is settled.  
**Supersedes:** 0.1.0 (prior version remains addressable by digest)

## 1. Purpose

Define the evolvable, evidence-driven process by which the receipted speculative graph is refined and developed through agentic orchestration.

The process applies the same DLC discipline to itself that it applies to the system under development. Observed mismatches between provisional directions and later settlements generate LearningEvents that may propose amendments. Amendments are themselves claims and are settled only by explicit evidence.

No final rendering of the graph system is produced under this specification version.

## 2. Scope

### In scope
- Orchestration of refinement and development activities
- Production, gating, and evolution of BRD, FRD, PRD, ADRs, SPEC, PROCESS, and supporting schemas
- Parallel speculative evidence collection with content-addressed response receipts
- Deterministic four-state settlement
- LearningEvent emission and controlled self-amendment of the process
- Explicit quarantine of unresolved or competing claims
- Separation of structural completeness from authority and empirical proof

### Out of scope
- Production implementation or final rendering of the graph system
- Any implication that a structural pass, receipt, confidence score, or document constitutes approval or truth
- Automatic mutation of canonical artifacts

## 3. Core Invariants (non-negotiable until settled amendment)

1. **Structure ≠ authority.** A document, receipt, gate pass, or model output does not establish that a claim is approved or empirically true.
2. **Canonical resolution is centralized.** Exactly one active SPEC root and one active PROCESS definition exist for any concern. Competing candidates are quarantined.
3. **Unresolved claims are quarantined.** They may be recorded and may generate evidence-collection tasks, but must not be used as premises.
4. **Settlement is evidence-driven only.** Confidence, structural completeness, and provisional direction never alter settlement state.
5. **Missing evidence is neutral.** TIMEOUT, MISSING, UNAVAILABLE, and MALFORMED observations contribute no sign.
6. **The process is evolvable.** LearningEvents may propose amendments. Only a settled PASS amendment may modify process definitions, gates, or invariants.
7. **Receipts are content-addressed.** Every significant observation, response, settlement, and learning event is identified by the SHA-256 digest of its canonical payload. Mutation creates a new object.
8. **History is recoverable.** Prior versions remain addressable after any amendment.
9. **Provisional answers are permitted but inert.** A confidence contract may allow early emission of a direction; the direction is stored as a response receipt and does not settle the claim.
10. **No silent divergence.** Any change to a canonical artifact must be receipted and, if load-bearing, settled.

## 4. Four-State Settlement (inherited from SIES)

| State | Condition |
|-------|-----------|
| **INDETERMINATE** | No explicit directional evidence, or required sources missing |
| **PASS** | Explicit supporting evidence present and required sources satisfied |
| **FAIL** | Explicit contradicting evidence present (and no unresolved conflict) |
| **CONFLICT** | Both explicit supporting and contradicting evidence present |

Explicit = status ∈ {PASS, FAIL}. All other statuses are neutral.

## 5. Process Claims Are First-Class

Claims about the process itself (“Gate 3 criteria are sufficient”, “this amendment improves recoverability”) are settled by the same rules as claims about the graph system. The orchestration layer does not receive special exemption.

## 6. Gate Model

Gates are evidence checkpoints, not authority grants.

Initial gates (amendable via settled LearningEvent):

| Gate | Claim (structural) | Minimum evidence |
|------|--------------------|------------------|
| 0 | Structure exists | SPEC-001 + PROCESS present and consistent |
| 1 | Requirements drafts complete | BRD + FRD + PRD consistent with SPEC |
| 2 | Architectural decisions recorded | ≥3 ADRs covering identity, provisional-vs-settlement, self-amendment |
| 3 | First orchestration loop with receipts | ≥30 response receipts + 1 settlement receipt from sketch or equivalent |
| 4 | Learning events reviewed | ≥1 LearningEvent examined; amendment settled or explicitly quarantined |

Subsequent gates are defined by the process.

A gate may be marked structurally complete without being treated as approved.

## 7. Self-Adjustment Mechanism (detailed)

1. A LearningEvent is emitted when:
   - Provisional direction ≠ settled state, or
   - A gate produces an outcome that contradicts its stated criteria, or
   - New explicit evidence arrives that changes a previously settled claim.
2. The LearningEvent is content-addressed and immutable.
3. An agent or human may draft an AmendmentProposal (a new Claim) referencing the LearningEvent.
4. The AmendmentProposal is settled using normal four-state rules.
5. Only a settled PASS amendment may update:
   - Gate criteria or evidence thresholds
   - Role definitions
   - Confidence contract parameters
   - Non-core process text
   - (Rare) an invariant — requires higher evidence threshold, currently quarantined as Q-001
6. The update produces a new content-addressed version of the affected artifact. The prior digest remains valid.
7. No automatic or confidence-driven mutation is permitted.

## 8. Quarantine

An item enters quarantine when:
- It is a competing canonical candidate
- It is load-bearing and lacks explicit supporting evidence
- Its settlement state is CONFLICT or INDETERMINATE and it is proposed as a premise
- It is an unresolved AmendmentProposal

Quarantined items are listed in QUARANTINE.md (or successor) and may be referenced by ID only.

## 9. Receipt and Schema Requirements

All receipts conform to RECEIPT-SCHEMA.md.  
Identity function:

```text
receipt_id = kind + ":sha256:" + hex(sha256(canonical_json(payload)))
```

## 10. Roles (agentic, non-exclusive)

- **Orchestrator** — schedules work, collects receipts, maintains process state
- **Spec Author** — produces or amends artifacts
- **Evidence Collector / Node** — emits EvidenceObservation + ResponseReceipt
- **Settler** — deterministic; never uses confidence
- **Learning Agent** — emits LearningEvents
- **Quarantine Steward** — enforces isolation of unresolved claims

Roles may be human, agent, or hybrid. Each action is receipted.

## 11. Non-Goals

- Production-ready graph implementation
- Treating any artifact in this set as approved or true
- Freezing the process against future settled amendments
- Requiring LangGraph, containers, or external databases for Gate 3

## 12. References

- SIES / GDS-RSI prototype (four-state settlement, content-addressed receipts, LearningEvents)
- DLC Truth-Integrity Audit (2026-09-20) — canonical resolution, structure ≠ authority
- Document Deterministics / Memory Atomization (spines, provenance)
- Unlazy discipline (depth-first completion)
- Existing sketch: `sies-langgraph-sketch/`

## 14. Approved Extensions (v0.3.0)

The following capabilities are now in scope as structural extensions (still not final system renderings):

- Executable Gate 3/4 harness that emits Gate3Evidence + MetricsReceipt (see GATE-3-HARNESS.md)
- Callable Quarantine Steward (see QUARANTINE-STEWARD.md)
- LearningEvent → AmendmentProposal template (see AMENDMENT-TEMPLATE.md)
- Loadable ConfidenceContract JSON derived from CONFIDENCE-CONTRACT.md
- Scale-probe mode (30/100/300) inside the harness
- Receipt citation rules: outer node identity required, inner digests optional (ADR-006).  
- Phase-by-phase alignment review (PHASE-REVIEW.md) drives incremental refinement.

These extensions produce evidence and receipts. They do not alter the core invariants.

This document is content-addressed. Future amendments produce new digests. The canonical designation is itself a settled claim.

---

**Disposition:** Structure only (v0.2.0). Requires Gate 0 consistency evidence.  
**Next:** Execute minimal loop (GATE-3-ORCHESTRATION-LOOP.md) to produce Gate 3 receipts.
