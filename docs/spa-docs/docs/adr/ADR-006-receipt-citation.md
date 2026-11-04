# ADR-006 — Receipt Citation Rules (Outer Required, Inner Optional)

**Status:** Proposed  
**Date:** 2026-11-03  
**Canonical parent:** SPEC-001  
**Related:** ADR-001, ADR-004, ADR-005, RECEIPT-SCHEMA.md

## Context

Receipts must identify the node that produced an observation. With both an outer MKZ digest and inner object digests available, we need a clear rule for what is required versus optional.

## Decision

- Every ResponseReceipt and SettlementReceipt MUST cite the outer node identity (MKZ archive SHA-256 or stub equivalent).
- Citation of one or more inner digests is OPTIONAL but RECOMMENDED when the observation or mismatch is attributable to specific objects.
- LearningEvent MAY include an `inner_digest_changes` array:
  ```json
  "inner_digest_changes": [
    {"path": "spines/document.md", "old": "sha256:…", "new": "sha256:…"}
  ]
  ```
- Gate3Evidence MAY include `manifest_digest` when a manifest is present.
- Absence of inner citations does not invalidate a receipt. Presence of incorrect inner citations is a MALFORMED observation.

## Consequences

- Graph and settlement continue to key off the single outer identity.
- Provenance and debugging gain optional precision.
- Stub path (no manifest) remains fully valid.
- Future harness or MKZ-backed nodes can populate the optional fields without schema breakage.

## Alternatives Considered

- Require inner citations — rejected; breaks stub compatibility and adds unnecessary burden.
- Forbid inner citations — rejected; loses the value of the inner layer.

## Evidence

Consistent with ADR-005 and the “outer = node identity” rule. No contradicting evidence.

---

**Disposition:** Proposed structural rule.
