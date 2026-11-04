# ADR-004 — MKZ as the Content-Addressed Container for Node Payloads

**Status:** Proposed — Gate 2 candidate  
**Date:** 2026-11-03  
**Canonical parent:** SPEC-001  
**Related:** ADR-001, EXTENSION-POINTS.md, https://github.com/gitspoked/mkz

## Context

Graph nodes require a stable, content-addressed identity for their memory + tools payload. The existing sketch uses a simple SHA-256 of a JSON blob. We already have a purpose-built container format in gitspoked/mkz that provides:

- End-to-end SHA-256 integrity
- Reversible transform (autocol) that preserves bit-exact round-trip
- Never-worse gate (falls back rather than expanding)
- Streaming, tar-style packaging suitable for structured data (markdown spines, tool descriptors, receipts)

## Decision

Adopt MKZ archives as the canonical on-disk / in-flight representation of a node’s memory + tools payload.

- Node identity = SHA-256 of the MKZ archive bytes (or the end-to-end digest already carried by the format).
- The sketch’s current JSON SHA remains a valid stub identity for Gate 3.
- Replacement of the stub by an MKZ-backed node is an extension-point swap (see EXTENSION-POINTS.md); settlement and receipt contracts are unchanged.

## Consequences

- Node payloads gain a real container format with integrity and reversible packing.
- Existing MKZ tooling (Rust CLI, C port) can be used to pack/unpack node memory without new code.
- Identity remains content-addressed; mutation still creates a new object.
- Gate 3 can still be satisfied with stubs; MKZ becomes the preferred path once the harness is stable.

## Alternatives Considered

- Plain tar + external SHA — rejected; MKZ already supplies the integrity and never-worse properties.
- Language-specific serialization only — rejected; does not give a portable container.
- Defer container choice indefinitely — rejected; we already have a working format in-repo.

## Evidence

- gitspoked/mkz README, FORMAT.md, and implementation (Rust + C) demonstrate SHA-256 integrity and reversible packing.
- Aligns with ADR-001 (content-addressed identity) and the original “MKZ containers as graph nodes” requirement.
- No contradicting evidence observed.

---

**Disposition:** Proposed structural decision. May be settled or amended via the normal LearningEvent path. Does not require immediate implementation for current gates.
