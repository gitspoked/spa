# PHASE-REVIEW — Alignment of Phases, Objects, and Flows to DLC Objectives

**Status:** Review + refinement direction  
**Version:** 0.1.0  
**Date:** 2026-11-03  
**Authority:** None. Structure only.  
**Canonical parent:** SPEC-001

## DLC Objectives (reminder)

1. Structure ≠ authority / empirical proof  
2. Canonical resolution (single root)  
3. Evidence-only four-state settlement (INDETERMINATE / PASS / FAIL / CONFLICT)  
4. Content-addressed identity (outer node + inner objects)  
5. Self-adjustment only via settled LearningEvents  
6. Quarantine of unresolved or competing claims  
7. Evolvable process; no premature final renderings  
8. Receipts for every significant action  
9. MKZ as container; inner manifest as identity layer  

---

## Phase 0 — Structure (Gate 0)

**Objects:** SPEC-001, PROCESS, GATES, QUARANTINE, README  
**Flow:** Documents exist and are mutually consistent  

**Alignment:** Strong. All declare “Authority: None.” Canonical root is explicit.  
**Gap:** No machine-checkable consistency receipt yet.  
**Refinement:** Add a ConsistencyReceipt (digest of the set of canonical doc digests) as optional Gate 0 evidence. Still structural only.

---

## Phase 1 — Requirements (Gate 1)

**Objects:** BRD, FRD, PRD  
**Flow:** Drafts complete, traceability present, open questions quarantined  

**Alignment:** Good. FR-001–FR-016 now cover harness, steward, amendment template.  
**Gap:** Inner identity (ADR-005) not yet reflected in functional requirements.  
**Refinement:** Add FR-017 (inner manifest) and FR-018 (outer vs inner reference rules).

---

## Phase 2 — Architecture (Gate 2)

**Objects:** ADR-001 (identity), ADR-002 (provisional vs settlement), ADR-003 (self-amendment), ADR-004 (MKZ outer), ADR-005 (inner layer)  
**Flow:** Decisions recorded with alternatives and consequences  

**Alignment:** Strong after ADR-004/005.  
**Gap:** No ADR yet for how receipts cite outer vs inner digests.  
**Refinement:** ADR-006 — Receipt citation rules (outer required, inner optional but recommended for provenance).

---

## Phase 3 — Execution / Evidence (Gate 3)

**Objects:** ContentAddressedNode (stub), DeterministicSettler, ResponseReceipt, SettlementReceipt, Gate3Evidence, MetricsReceipt, harness  
**Flow:** Parallel nodes → observations → settler → receipts + metrics  

**Alignment:** Good for stubs. MKZ + inner layer defined but not exercised.  
**Gap:** Harness does not yet emit or verify an inner manifest.  
**Refinement:** Extend harness to optionally pack a minimal MKZ (or simulate the manifest) and include inner digests in Gate3Evidence. Keep stub path as default.

---

## Phase 4 — Learning / Amendment (Gate 4)

**Objects:** LearningEvent, AmendmentProposal (template), Quarantine Steward  
**Flow:** Mismatch → LearningEvent → template proposal → settle → update or quarantine  

**Alignment:** Solid. Template exists. Steward is specified.  
**Gap:** No explicit link from an inner-digest change to a LearningEvent rationale.  
**Refinement:** Extend LearningEvent schema with optional `inner_digest_changes[]`. Amendment template already allows targeting a specific inner object.

---

## Cross-cutting Objects

| Object | DLC objective served | Status | Refinement |
|--------|----------------------|--------|------------|
| Claim | Evidence-driven settlement | Defined | None |
| ResponseReceipt | Provisional answer, content-addressed | Defined | Cite outer identity; optional inner |
| SettlementReceipt | Four-state outcome | Defined | None |
| LearningEvent | Self-adjustment signal | Defined | Add optional inner changes |
| MKZ archive | Outer container identity | ADR-004 | None |
| Inner manifest | Per-object identity | ADR-005 | Add to harness + FR |
| QuarantineDecision | Prevent premise misuse | Specified | Implement check in harness path |
| ConfidenceContract | Provisional permission | Defined | Already loadable |

---

## Cross-cutting Flows

| Flow | Alignment | Adjustment |
|------|-----------|------------|
| Full lifecycle | Matches PROCESS cycle | Add optional inner-manifest step before packing |
| CONFLICT | Correctly preserves both sides, quarantines as premise | Cite which inner objects contributed PASS vs FAIL |
| INDETERMINATE | Holds gate, schedules more evidence | None |
| Self-adjustment success | Settled amendment → new digest | Allow amendment to target inner manifest rules |
| Self-adjustment quarantine | Unresolved proposal isolated | None |
| Scale probe | Defined in harness | Record inner-churn rate as additional metric |

---

## Direction to expand

1. **FR-017 / FR-018** — Inner manifest and citation rules.  
2. **ADR-006** — Receipts cite outer (required) and inner (optional).  
3. **Schema extensions** — LearningEvent may list inner digest changes; Gate3Evidence may include manifest_digest.  
4. **Harness extension point** — Optional MKZ pack + manifest verification (stub remains default).  
5. **Provenance note** — Inner digests become the natural IDs for Document Deterministics atoms.  
6. **Metric** — Inner-churn rate (changed inner digests / total inner objects per outer update).

All expansions remain structural, evolvable, and subject to the same settlement and quarantine rules.

---

**Disposition:** Review complete. Refinements below are proposed for inclusion; they do not alter core invariants.
