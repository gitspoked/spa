# ADR-001 — Content-Addressed Identity for All Process Artifacts and Receipts

**Status:** Accepted (structural) — Gate 2 candidate  
**Date:** 2026-11-03  
**Canonical parent:** SPEC-001

## Context

The system must support evolvable process definitions, parallel speculative execution, and reconstructible history. Mutable identities make it impossible to know which version of a claim, gate criterion, or receipt was used.

## Decision

Every significant artifact and receipt shall be identified by the SHA-256 digest of its canonical serialized payload. Mutation creates a new object; prior objects remain addressable.

## Consequences

- History is append-only and recoverable.
- Competing versions are distinguishable by digest.
- Canonical resolution reduces to designating a digest.
- Storage and transmission must preserve exact bytes used for the digest.

## Alternatives Considered

- Mutable database rows with version columns — rejected; versions can be overwritten or ambiguously referenced.
- UUIDs without content binding — rejected; does not guarantee the content matches the identifier.

## Evidence

Consistent with SIES prototype and Document Deterministics memory atomization. No contradicting evidence observed.

---

**Disposition:** Structural decision. Subject to later settlement if contradicting evidence appears.
