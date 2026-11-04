# FRD — Functional Requirements: Agentic Orchestration Process

**Status:** Draft — Gate 1 candidate  
**Version:** 0.2.0 (expanded)  
**Date:** 2026-11-03  
**Authority:** None. Structure only.  
**Canonical parent:** SPEC-001

## 1. Functional Overview

The system shall provide agentic orchestration of the refinement and development process for the receipted speculative graph, including:

- Canonical artifact management
- Parallel speculative evidence collection
- Deterministic four-state settlement
- Provisional answer emission under confidence contracts
- LearningEvent generation
- Controlled self-amendment
- Quarantine enforcement
- Full recoverability of history

## 2. Functional Requirements (expanded)

### FR-001 — Canonical Artifact Management
The system shall maintain exactly one active SPEC root and one active PROCESS definition.  
Competing candidates shall be detected, quarantined, and resolvable only by a settled ResolutionClaim that designates a canonical digest.

### FR-002 — Content-Addressed Receipts
Every significant action shall produce a receipt whose identity is  
`kind:sha256:` + hex(SHA-256(canonical JSON payload)).  
Kinds include: response, settlement, learning, amendment, orchestration, quarantine, resolution, artifact.

### FR-003 — Four-State Settlement
The system shall settle claims exclusively from explicit evidence observations according to:

- CONFLICT if both explicit PASS and explicit FAIL exist
- FAIL if explicit FAIL exists and no CONFLICT
- PASS if explicit PASS exists and required sources are satisfied
- INDETERMINATE otherwise

Confidence, structural completeness, and provisional direction shall have zero effect on settlement state.

### FR-004 — Provisional Answers
The system may emit a provisional direction when a recorded ConfidenceContract is satisfied.  
The provisional answer shall be stored solely as a ResponseReceipt and shall not be readable by the Settler as evidence.

### FR-005 — Learning Events
The system shall emit a LearningEvent when:
- provisional direction ≠ settled state, or
- a gate outcome contradicts its criteria, or
- new explicit evidence changes a prior settlement.

The event shall reference both the response and settlement receipts.

### FR-006 — Amendment Proposal and Settlement
A LearningEvent may trigger an AmendmentProposal (new Claim).  
The proposal shall be settled with normal four-state rules.  
Only a PASS settlement may cause a new version of a process artifact to be written.  
Prior versions remain addressable.

### FR-007 — Gate Evaluation
The system shall evaluate each gate claim, record the evidence used, and produce an OrchestrationReceipt.  
Structural completeness and settlement state shall be recorded separately.

### FR-008 — Quarantine
The system shall isolate:
- competing canonical candidates
- load-bearing claims lacking explicit evidence
- CONFLICT or INDETERMINATE claims proposed as premises
- unresolved AmendmentProposals

Quarantined items shall be unusable as premises. Isolation actions produce QuarantineReceipts.

### FR-009 — Parallel Evidence Collection
Evidence collection for any claim (system or process) may be performed by N nodes/agents concurrently.  
Each shall emit its own ResponseReceipt + EvidenceObservation.  
N ≥ 30 is sufficient for Gate 3 stub demonstration.

### FR-010 — Recoverability
All prior versions of artifacts and all receipts shall remain content-addressed and retrievable after any amendment or supersession.

### FR-011 — Schema Conformance
All receipts shall conform to RECEIPT-SCHEMA.md.  
Non-conformant payloads shall produce MALFORMED observations and shall not settle parent claims.

### FR-012 — Stub Execution Path
The system shall support full Gate 3 satisfaction using only the existing `sies-langgraph-sketch` stub nodes and in-memory settler.  
No external database, LangGraph runtime, or container is required for initial gates.

### FR-013 — Extension Points
The system shall define clear replacement boundaries so that:
- stub nodes may be replaced by LangGraph nodes or containerized MKZ executors
- in-memory receipt logs may be replaced by FalkorDB, object store, or Git
- stub memory may be replaced by Document Deterministics atomized spines

without altering settlement or receipt contracts.

## 3. Non-Functional Requirements (structural)

- Receipt serialization must be deterministic (sorted keys, stable separators).
- Audit trail must permit full reconstruction of any claim’s evidence → settlement → learning → amendment path.
- Process must remain executable after any single settled amendment.
- No single role may both emit provisional direction and settle the same claim in a production configuration (separable in stubs).

### FR-014 — Gate 3/4 Harness
The system shall provide an executable harness that, given a claim and node count, produces ResponseReceipts, a SettlementReceipt, a Gate3Evidence receipt, and a MetricsReceipt. Scale-probe mode (30/100/300) shall be supported.

### FR-015 — Quarantine Steward
The system shall expose a callable steward.check(claim_id) that returns whether the claim may be used as a premise and emits a QuarantineReceipt on every blocking decision.

### FR-017 — Inner Manifest
When a node payload is an MKZ archive, it SHALL contain a canonical manifest listing each object’s path, SHA-256 digest, and role. The manifest itself SHALL have a manifest_digest. Stub payloads are exempt.

### FR-018 — Receipt Citation
ResponseReceipt and SettlementReceipt SHALL cite the outer node identity. Inner digests MAY be cited. LearningEvent MAY record inner_digest_changes. See ADR-006.

## 4. Traceability (expanded)

| FR | SPEC | PROCESS | ADR | Schema |
|----|------|---------|-----|--------|
| FR-001 | §3.2, §8 | §6 | — | — |
| FR-002 | §3.7, §9 | §7 | ADR-001 | RECEIPT-SCHEMA |
| FR-003 | §4 | §3 | ADR-002 | — |
| FR-004 | §3.9, §5 | §3 | ADR-002 | ResponseReceipt |
| FR-005 | §7 | §5 | ADR-003 | LearningEvent |
| FR-006 | §7 | §5 | ADR-003 | AmendmentProposal |
| FR-007 | §6 | §4 | — | — |
| FR-008 | §8 | §8 | — | — |
| FR-009 | §5 | §3 | — | — |
| FR-010 | §3.8 | §5 | ADR-001 | — |
| FR-011 | §9 | §7 | — | RECEIPT-SCHEMA |
| FR-012 | §11 | §10 | — | GATE-3 |
| FR-013 | §2 | §10 | — | — |

## 5. Open Functional Questions (quarantined)

| ID | Question | Status |
|----|----------|--------|
| Q-001 | Evidence threshold for invariant amendment | Quarantined |
| Q-002 | Persistence backend at 300–3000 nodes | Quarantined |
| Q-003 | Mandatory human-in-the-loop points | Quarantined |
| Q-004 | Exact LearningEvent field optionality | Quarantined |
| Q-005 | Maximum acceptable CONFLICT rate before gate hold | Quarantined |

---

**Disposition:** Draft v0.2.0. Requires Gate 1 consistency review.  
**Next:** Execute Gate 3 loop; collect first LearningEvents.
