# QUARANTINE-STEWARD — Callable Quarantine Enforcement

**Status:** Draft  
**Version:** 0.1.0  
**Date:** 2026-11-03  
**Authority:** None.  
**Canonical parent:** SPEC-001  
**Related:** QUARANTINE.md, FR-008, PROCESS §8

## 1. Purpose

Turn the quarantine rule into a callable check that the orchestrator must invoke before using any prior claim as a premise.

## 2. Interface

```text
steward.check(claim_id) → QuarantineDecision
```

```json
{
  "claim_id": "...",
  "usable_as_premise": false,
  "reason": "CONFLICT | INDETERMINATE | competing-canonical | unresolved-amendment | no-explicit-evidence",
  "quarantine_receipt_id": "quarantine:sha256:..."
}
```

## 3. Rules (must match QUARANTINE.md)

- COMPETING canonical → usable_as_premise = false
- Load-bearing + no explicit evidence → false
- Settlement CONFLICT or INDETERMINATE and proposed as premise → false
- Unresolved AmendmentProposal → false
- Otherwise → true

## 4. Side Effect

Every blocking decision emits a QuarantineReceipt (content-addressed).

## 5. Orchestrator Obligation

Before any claim is used as a premise in a new settlement or amendment, the orchestrator shall call the steward. A missing call is itself a process defect that may generate a LearningEvent.

---

**Disposition:** Structural. Enforcement mechanism only.
