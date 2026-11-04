# PROCESS — DLC-Driven Agentic Orchestration with Self-Adjustment

**Status:** Draft — Gate 0  
**Version:** 0.2.0 (expanded)  
**Date:** 2026-11-03  
**Authority:** None. Structure only.  
**Canonical parent:** SPEC-001  
**Supersedes:** 0.1.0

## 1. Intent

Provide a repeatable, evidence-driven, self-adjusting process for refining and developing the receipted speculative graph. The process is a first-class claim subject to the same settlement rules it enforces.

## 2. Roles and Responsibilities

| Role | Responsibilities | Receipts produced |
|------|------------------|-------------------|
| Orchestrator | Maintain process state, schedule cycles, collect receipts, advance or hold gates | OrchestrationReceipt |
| Spec Author | Draft or amend BRD/FRD/PRD/ADR/SPEC/PROCESS | ArtifactReceipt (content-addressed) |
| Evidence Collector / Node | Execute against a claim; emit observation | ResponseReceipt + EvidenceObservation |
| Settler | Apply four-state rules exclusively from explicit evidence | SettlementReceipt |
| Learning Agent | Compare provisional vs settled; emit mismatches | LearningEvent |
| Quarantine Steward | Isolate competing or unresolved claims; prevent premise use | QuarantineReceipt |
| Human Process Owner | May act in any role; all actions still receipted | (same as role) |

Roles are not mutually exclusive. A single agent may fulfill multiple roles in a stub demonstration.

## 3. Detailed Cycle

```
┌─────────────┐
│ Claim C     │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐     optional
│ Provisional predict │──────────────► ResponseReceipt (direction + confidence)
└──────┬──────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Parallel Evidence Collection        │
│ Node_1 … Node_N                     │
│ each → ResponseReceipt_i + Obs_i    │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────┐
│ Deterministic       │
│ Settler             │──► SettlementReceipt (INDETERMINATE|PASS|FAIL|CONFLICT)
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Learning comparison │──► LearningEvent (if mismatch or unexpected)
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Amendment?          │──► AmendmentProposal (new Claim)
│                     │    └─► settle independently
└──────┬──────────────┘
       │
       ▼
   Gate advance / hold / amend process
```

Steps marked parallel may execute concurrently. Settlement remains deferred until explicit evidence is collected.

## 4. Gate Progression Rules (expanded)

### Structural completeness
A gate claim may be marked structurally complete when:
- Required artifacts exist and are mutually consistent
- Internal cross-references resolve
- All premises used are either settled PASS or explicitly quarantined
- A consistency checklist receipt exists

Structural completeness ≠ approval.

### Progression
Progression to the next gate requires:
1. Explicit evidence receipt(s) supporting the progression claim, and
2. Settlement state of the progression claim = PASS,  
   **or** the claim is explicitly accepted as provisional under a recorded confidence contract (the contract itself is receipted and does not settle the claim).

### Holding
If settlement = INDETERMINATE or CONFLICT, the gate is held. Additional evidence-collection tasks may be scheduled. The hold is itself receipted.

## 5. Self-Adjustment Protocol (expanded)

### Trigger conditions
- Provisional direction ≠ settled state
- Gate outcome contradicts its written criteria
- New explicit evidence arrives for a previously settled claim
- Repeated INDETERMINATE results suggest criteria are too strict or evidence sources are insufficient

### Protocol steps
1. LearningEvent emitted (content-addressed, immutable).
2. Learning Agent or human drafts AmendmentProposal referencing the event.
3. AmendmentProposal is treated as a normal Claim.
4. Parallel evidence may be collected on the amendment itself.
5. Settler produces SettlementReceipt for the amendment.
6. If PASS:
   - New version of the affected artifact is written
   - Prior version remains addressable by old digest
   - Canonical designation is updated via a resolution receipt
7. If FAIL / CONFLICT / INDETERMINATE:
   - Amendment is quarantined or rejected
   - Process definition unchanged

### Invariant amendment
Amending a core invariant (Section 3 of SPEC-001) requires a higher evidence threshold. The exact threshold is currently quarantined (Q-001). Until resolved, invariant amendments are held.

## 6. Canonical Resolution Procedure

1. Detect competing candidates (multiple SPEC roots, multiple PROCESS definitions, conflicting ADRs on the same decision).
2. Quarantine all but one provisional candidate.
3. Raise a ResolutionClaim: “Digest D is the canonical artifact for concern X”.
4. Settle the ResolutionClaim with explicit evidence (human designation, prior settled policy, etc.).
5. On PASS, record the canonical digest. All other candidates remain quarantined or are marked superseded (still addressable).

## 7. Receipt Requirements (expanded)

Every significant action produces a receipt containing at minimum:
- kind (response | settlement | learning | amendment | orchestration | quarantine | resolution)
- receipt_id (content-addressed)
- claim_id or target
- actor identity (content-addressed where applicable)
- timestamp (ISO-8601 UTC)
- payload digest
- references to prior receipts (evidence_ids, triggered_by, etc.)

Receipts are append-only. See RECEIPT-SCHEMA.md for concrete payloads.

## 8. Quarantine Rules (expanded)

| Condition | Action |
|-----------|--------|
| Competing canonical candidate | Quarantine; raise ResolutionClaim |
| Load-bearing claim with no explicit evidence | Quarantine; schedule evidence collection |
| CONFLICT settlement proposed as premise | Quarantine until resolved |
| Unresolved AmendmentProposal | Quarantine |
| MALFORMED observation | Neutral for parent; may quarantine source node |

Quarantine list is maintained in QUARANTINE.md (content-addressed on change).

## 9. Current Gate Status (living)

| Gate | Claim | State | Evidence | Notes |
|------|-------|-------|----------|-------|
| 0 | Structure exists | INDETERMINATE | SPEC-001 v0.2.0 + PROCESS v0.2.0 | Consistency check pending |
| 1 | BRD/FRD/PRD complete | — | Drafts exist | — |
| 2 | ADRs recorded | — | ADR-001..003 exist | — |
| 3 | First loop with receipts | — | Sketch available | Execute GATE-3 spec |
| 4 | Learning events reviewed | — | — | — |

## 10. Stub vs Production

Gate 3 may be satisfied entirely with stub nodes (`ContentAddressedNode` in the sketch).  
Replacement of stubs by LangGraph nodes, containerized MKZ executors, or real atomized memory is an extension, not a prerequisite.

## 12. Executable Gate 3/4 Path

Gate 3 evidence is produced by the harness defined in GATE-3-HARNESS.md.  
Gate 4 reviews the resulting LearningEvents using the template in AMENDMENT-TEMPLATE.md.  
Before any claim is reused as a premise, the orchestrator calls the Quarantine Steward (QUARANTINE-STEWARD.md).

## 13. Non-Goals

- Automatic process mutation
- Confidence-based settlement
- Final system renderings
- Requiring external infrastructure for initial gates

---

**Disposition:** Structure only (v0.2.0). Self-adjustment defined and ready for first LearningEvent.  
**Next:** Execute minimal orchestration loop to generate Gate 3 receipts.
