# ADR-007 — Evidence-Grounded Precision Loop

**Status:** Proposed  
**Date:** 2026-11-03  
**Canonical parent:** SPEC-001  
**Related:** ADR-005, ADR-006, RECEIPT-SCHEMA.md, FRD

## Context

Precision, depth, and completeness improve most when every decisive observation is (1) attributed to an exact inner digest and (2) accompanied by an explicit counter-evidence attempt.

## Decision

For any claim marked high-precision (or when a confidence contract sets `require_counter_evidence: true`):

1. Every explicit PASS or FAIL observation that influences settlement MUST cite `source_inner_digest`.
2. A decisive supporting observation MUST be paired with either:
   - an explicit counter-observation (FAIL or PASS from a different node identity), or
   - a `NO_COUNTER_EVIDENCE` receipt from a different node identity.
3. Absence of the required counter pair leaves the claim INDETERMINATE (or blocks high-precision PASS).
4. Ordinary claims remain on the original four-state rules.
5. All new fields are content-addressed and cacheable by inner digest.

## Consequences

- Settled PASS/FAIL for high-precision claims carry provenance and a recorded refutation attempt.
- Attention and branching naturally expand toward counter-nodes.
- Cache re-uses prior counter-searches on the same inner digest.
- Stub nodes remain valid by emitting a synthetic inner digest.
- Settlement is still performed only by the settler from explicit observations.

## Alternatives Considered

- Majority vote — rejected; erases minority explicit evidence.
- Confidence-only precision — rejected; violates evidence-only settlement.
- Optional counter-evidence — rejected for high-precision mode; completeness requires the attempt to be explicit.

## Evidence

Aligns with ADR-005 (inner identity), ADR-006 (citation), and the goal of maximizing precision, depth, and completeness without altering core invariants.

---

**Disposition:** Proposed. Opt-in via claim flag or confidence contract. Does not change default Gate 3 stub behavior.
