# CONFIDENCE-CONTRACT — Provisional Answer Rules

**Status:** Draft — supporting Gate 3  
**Version:** 0.1.0  
**Date:** 2026-11-03  
**Authority:** None. Structure only.  
**Canonical parent:** SPEC-001  
**Related:** ADR-002, FR-004

## 1. Purpose

Define the conditions under which a provisional direction may be emitted before settlement.  
The contract never settles a claim.

## 2. Contract Fields

| Field | Type | Default | Meaning |
|-------|------|---------|---------|
| min_confidence | float | 0.85 | Minimum predictor confidence |
| min_explicit_observations | int | 1 | Minimum count of explicit (PASS/FAIL) observations |
| max_conflict_ratio | float | 0.0 | Optional; if >0, provisional blocked when conflict ratio exceeds |
| expiry | duration or null | null | Optional time bound |

## 3. Permission Rule

```
answer_permitted =
  prediction.direction is not None
  AND prediction.confidence >= min_confidence
  AND explicit_count >= min_explicit_observations
  AND (max_conflict_ratio == 0 OR conflict_ratio <= max_conflict_ratio)
```

If permitted, a ResponseReceipt is emitted with `answer_permitted: true`.  
Settlement proceeds independently.

## 4. Recording

Every use of a contract produces a receipt referencing the contract digest.  
Contract definitions are themselves content-addressed and amendable only via settled claim.

## 5. Default Stub Contract (Gate 3)

```yaml
min_confidence: 0.70
min_explicit_observations: 1
max_conflict_ratio: 0.0
```

Used by the existing sketch. May be tightened or relaxed by settled amendment.

---

**Disposition:** Structural. Does not grant authority to any provisional answer.
