# ADR-005 — Inner Identity Layer (MKZ-of-MKZ)

**Status:** Proposed — Gate 2 candidate  
**Date:** 2026-11-03  
**Canonical parent:** SPEC-001  
**Related:** ADR-001, ADR-004, gitspoked/mkz FORMAT.md, Document Deterministics spines

## Context

ADR-004 establishes the outer MKZ archive SHA as the node identity (container digest).  

Nodes also contain multiple independent objects:
- memory atoms / spines (document, subject, temporal, evidence, …)
- tool descriptors
- prior receipts or references
- configuration

Each of these must be individually content-addressed so that:
- a change to one atom does not require re-identifying unchanged siblings
- provenance and nearest/furthest-neighbor relations can cite stable inner digests
- the outer container digest still changes if any inner object changes (because the manifest or the bytes change)

This is an identity layer inside the container — an MKZ-of-MKZ.

## Decision

Every MKZ node payload SHALL contain a canonical manifest entry (path: `manifest.json` or `identity/manifest.json`) whose content is a content-addressed index:

```json
{
  "version": 1,
  "objects": [
    {
      "path": "spines/document.md",
      "digest": "sha256:…",
      "role": "memory-spine"
    },
    {
      "path": "tools/router.json",
      "digest": "sha256:…",
      "role": "tool"
    }
  ],
  "manifest_digest": "sha256:…"
}
```

Rules:
- Each listed object’s `digest` is the SHA-256 of its exact bytes inside the archive.
- `manifest_digest` is the SHA-256 of the canonical serialization of the `objects` array (sorted by path).
- The outer node identity remains the MKZ end-to-end SHA-256 (ADR-004). It transitively covers the manifest and all objects.
- Inner objects MAY themselves be MKZ archives (nested containers). Their digest is still the SHA-256 of their archive bytes.
- Stub nodes (plain JSON SHA) remain valid for Gate 3; they simply have a single implicit object.

## Consequences

- Fine-grained, stable identity for every atom/tool inside a node.
- Outer container digest still serves as the single node identity for graph edges and receipts.
- Mutation of any inner object produces a new outer digest (and a new manifest digest).
- Aligns with Document Deterministics atomization (each spine/atom can be an inner object).
- Existing MKZ tooling can pack the tree; only the manifest convention is new.
- Receipt and settlement contracts are unchanged; they continue to reference the outer node identity.

## Alternatives Considered

- Single flat SHA of concatenated payloads — rejected; loses per-object stability and provenance.
- External side-car index outside the MKZ — rejected; breaks the “container is the identity” property.
- Git tree objects only — rejected for now; MKZ is already the chosen container and is streaming/portable.

## Evidence

- MKZ FORMAT.md already supports multi-entry archives and end-to-end SHA-256.
- Document Deterministics describes typed atoms and spines that map directly to inner objects.
- No contradicting evidence.

---

**Disposition:** Proposed. Implements the “identity layer within” requirement. May be settled or refined via LearningEvent. Stub path remains open for current gates.
