# Agentic Orchestration of Receipted Speculative Graph Refinement

**Status:** Gate 0 structure (expanded)  
**Canonical root:** [docs/SPEC.md](docs/SPEC.md) (v0.2.0)  
**Date:** 2026-11-03

DLC-driven SDD/TDD artifacts defining the evolvable, self-adjusting process for refining the receipted speculative graph.  
All documents are structural only. None constitute approval or empirical proof.

## On-the-fly Diagram Utility

```bash
python3 diagram_util.py all
```

Writes Mermaid sources to `generated-diagrams/*.mmd` (render with any Mermaid tool).  
Static reference images live in `docs/images/`.

## Documents

| Document | Purpose | Version |
|----------|---------|---------|
| [docs/SPEC.md](docs/SPEC.md) | Canonical specification (SPEC-001) | 0.2.0 |
| [docs/PROCESS.md](docs/PROCESS.md) | Full cycle, roles, self-adjustment protocol | 0.2.0 |
| [docs/BRD.md](docs/BRD.md) | Business requirements | 0.1.0 |
| [docs/FRD.md](docs/FRD.md) | Functional requirements FR-001–FR-013 + traceability | 0.2.0 |
| [docs/PRD.md](docs/PRD.md) | Product requirements + Gate 1 criteria | 0.1.0 |
| [docs/GATES.md](docs/GATES.md) | Gate 0–4 definitions | 0.1.0 |
| [docs/GATE-3-ORCHESTRATION-LOOP.md](docs/GATE-3-ORCHESTRATION-LOOP.md) | Minimal executable loop for Gate 3 | 0.1.0 |
| [docs/RECEIPT-SCHEMA.md](docs/RECEIPT-SCHEMA.md) | Canonical receipt & LearningEvent schemas | 0.1.0 |
| [docs/CONFIDENCE-CONTRACT.md](docs/CONFIDENCE-CONTRACT.md) | Provisional answer rules | 0.1.0 |
| [docs/GATE-3-HARNESS.md](docs/GATE-3-HARNESS.md) | Executable Gate 3/4 harness + metrics | 0.1.0 |
| [docs/QUARANTINE-STEWARD.md](docs/QUARANTINE-STEWARD.md) | Callable quarantine enforcement | 0.1.0 |
| [docs/AMENDMENT-TEMPLATE.md](docs/AMENDMENT-TEMPLATE.md) | LearningEvent → AmendmentProposal template | 0.1.0 |
| [docs/QUARANTINE.md](docs/QUARANTINE.md) | Unresolved claims | living |
| [docs/adr/](docs/adr/) | ADR-001 identity, ADR-002 provisional vs settlement, ADR-003 self-amendment | — |

## Invariants

- Structure ≠ authority or empirical proof
- Settlement is evidence-driven only (four states)
- Process amends itself only via settled LearningEvents
- All significant objects are content-addressed
- Unresolved claims are quarantined
- History is recoverable

## Executable Path to Gate 3

```bash
cd sies-langgraph-sketch
python3 sketch.py
```

Produces response receipts + settlement receipt satisfying the structural evidence requirement in GATE-3-ORCHESTRATION-LOOP.md.

## Authority

None. These documents define structure only.

---

**Next:** Consistency review (Gate 1) → execute loop (Gate 3) → first LearningEvent review (Gate 4).
