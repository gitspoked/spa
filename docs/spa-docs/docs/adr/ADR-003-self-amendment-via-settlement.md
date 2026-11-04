# ADR-003 — Process Self-Amendment Only via Settled Learning Events

**Status:** Accepted (structural) — Gate 2 candidate  
**Date:** 2026-11-03  
**Canonical parent:** SPEC-001

## Context

The orchestration process must be able to evolve, yet uncontrolled mutation would recreate the canonical-resolution and authority problems identified in the DLC Truth-Integrity Audit.

## Decision

Process definitions, gate criteria, and invariants may be amended only by a claim that has been settled PASS on the basis of explicit evidence (normally a LearningEvent plus supporting observations). Prior versions remain content-addressed.

## Consequences

- Self-adjustment is possible and auditable.
- No automatic or confidence-driven mutation.
- Amendment claims are first-class and subject to the same four-state rules.
- Quarantine applies to unresolved amendment proposals.

## Alternatives Considered

- Direct agent rewrite of process documents — rejected; no settlement, no receipt trail.
- Human-only amendments — rejected as sole path; does not scale and still requires receipts.

## Evidence

Required by SPEC-001 invariants and PROCESS self-adjustment protocol. Aligns with audit finding that structure ≠ authority.

---

**Disposition:** Structural decision. Subject to later settlement if contradicting evidence appears.
