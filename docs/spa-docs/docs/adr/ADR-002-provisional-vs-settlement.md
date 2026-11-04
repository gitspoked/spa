# ADR-002 — Separation of Provisional Answer from Deterministic Settlement

**Status:** Accepted (structural) — Gate 2 candidate  
**Date:** 2026-11-03  
**Canonical parent:** SPEC-001

## Context

Agents and predictors can often produce a useful direction before all evidence has arrived. Allowing that direction to settle the claim would violate the evidence-only settlement invariant.

## Decision

A confidence contract may permit emission of a provisional direction (response receipt). Settlement state is determined solely by explicit evidence observations and remains independent of the provisional answer. Mismatches produce LearningEvents.

## Consequences

- Work can proceed speculatively.
- Settlement stays deterministic and auditable.
- Learning events provide the signal for process self-adjustment.
- Consumers must distinguish response receipts from settlement receipts.

## Alternatives Considered

- Confidence-weighted settlement — rejected; violates core invariant and DLC audit findings.
- Blocking until full evidence — rejected; prevents parallel speculative progress.

## Evidence

Directly inherited from SIES design. Sketch demonstrates the separation.

---

**Disposition:** Structural decision. Subject to later settlement if contradicting evidence appears.
