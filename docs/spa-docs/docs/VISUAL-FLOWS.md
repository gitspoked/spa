# VISUAL-FLOWS — Full Lifecycle, Scenarios, and Efficiency

**Status:** Draft — supporting  
**Version:** 0.1.0  
**Date:** 2026-11-03  
**Authority:** None. Structure only.  
**Canonical parent:** SPEC-001

Diagrams use Mermaid. They illustrate structure and possible paths. They do not constitute approval or empirical proof.

---

**Static image versions** (also in `docs/images/`):

![Full Lifecycle](images/lifecycle.jpg)

![Success PASS](images/success-pass.jpg)

![CONFLICT Scenario](images/conflict.jpg)

![Gate Progression](images/gates.jpg)

---

## 1. Full Lifecycle Overview

```mermaid
flowchart TD
    A[Claim C created] --> B{Confidence contract<br/>satisfied?}
    B -->|Yes| C[Emit provisional<br/>ResponseReceipt]
    B -->|No| D[Skip provisional]
    C --> E
    D --> E
    E[Parallel Evidence Collection<br/>Node 1..N] --> F[Collect Observations]
    F --> G[Deterministic Settler]
    G --> H{Settlement State}
    H -->|PASS| I[SettlementReceipt PASS]
    H -->|FAIL| J[SettlementReceipt FAIL]
    H -->|CONFLICT| K[SettlementReceipt CONFLICT]
    H -->|INDETERMINATE| L[SettlementReceipt INDETERMINATE]
    I --> M{Provisional ≠ Settled?}
    J --> M
    K --> M
    L --> M
    M -->|Yes| N[Emit LearningEvent]
    M -->|No| O[No LearningEvent]
    N --> P{Amendment proposed?}
    P -->|Yes| Q[Settle AmendmentProposal]
    Q -->|PASS| R[Update process artifact<br/>new digest]
    Q -->|other| S[Quarantine amendment]
    P -->|No| T[Continue]
    R --> U[Gate evaluation]
    S --> U
    O --> U
    T --> U
    U --> V{Gate progression<br/>claim settled PASS?}
    V -->|Yes| W[Advance gate]
    V -->|No| X[Hold gate<br/>schedule more evidence]
```

---

## 2. Success Scenario — Clean PASS

**Example claim:** “Gate 3 minimum of 30 response receipts is sufficient for stub demonstration.”

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant N as Nodes (30+)
    participant S as Settler
    participant L as Learning Agent

    O->>N: execute(claim)
    N-->>O: 28× MISSING/TIMEOUT<br/>2× explicit PASS
    O->>S: settle(observations)
    S-->>O: SettlementReceipt PASS
    Note over L: provisional was PASS<br/>settled PASS → no mismatch
    L-->>O: (no LearningEvent)
    O->>O: Gate 3 structurally complete<br/>progression claim PASS
```

**Outcome:** Settlement PASS, no LearningEvent, gate may advance.  
**Efficiency note:** High explicit-evidence yield relative to nodes run.

---

## 3. Failure Scenario — Explicit FAIL

**Example claim:** “Stub nodes alone prove production readiness.”

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant N as Nodes
    participant S as Settler

    O->>N: execute(claim)
    N-->>O: 5× explicit FAIL<br/>10× MISSING
    O->>S: settle
    S-->>O: SettlementReceipt FAIL
    Note over O: Provisional (if any) mismatched<br/>→ LearningEvent
    O->>O: Claim settled FAIL<br/>do not use as premise
```

**Outcome:** Settlement FAIL. Claim quarantined as premise. LearningEvent may propose tighter Gate 3 criteria or additional required evidence.  
**Efficiency note:** Early FAIL with few nodes is cheap; avoids wasted downstream work.

---

## 4. CONFLICT Scenario — Mixed Explicit Evidence

**Example:** Stacy/Stephanie-style competing observations on the same claim.

```mermaid
flowchart LR
    subgraph Evidence
        P[3× explicit PASS]
        F[2× explicit FAIL]
        M[25× MISSING/TIMEOUT]
    end
    Evidence --> Settler
    Settler --> CONFLICT[SettlementReceipt<br/>CONFLICT]
    CONFLICT --> Q[Quarantine as premise]
    CONFLICT --> LE[LearningEvent<br/>mismatch or unexpected]
    LE --> AP[AmendmentProposal<br/>e.g. require source weighting<br/>or additional nodes]
```

**Outcome:** CONFLICT. Neither side erased. Both receipts remain. Claim cannot be used as a settled premise until resolved by further evidence or explicit policy.  
**Efficiency note:** CONFLICT is informative; it surfaces the need for better evidence or refined criteria rather than silent error.

---

## 5. INDETERMINATE Scenario — Insufficient Explicit Evidence

```mermaid
flowchart TD
    A[64 stub nodes] --> B[60× MISSING/TIMEOUT<br/>4× weak]
    B --> C[Settler]
    C --> D[INDETERMINATE]
    D --> E[Hold gate]
    E --> F[Schedule additional<br/>evidence collection<br/>or different node types]
    F --> G[Re-run loop]
```

**Outcome:** INDETERMINATE. Gate held. Process remains correct; more evidence required.  
**Efficiency note:** Cheap to detect. Prevents false progression.

---

## 6. Self-Adjustment Success Path

```mermaid
flowchart TD
    A[LearningEvent:<br/>provisional PASS<br/>settled CONFLICT] --> B[AmendmentProposal:<br/>Add conflict_ratio check<br/>to confidence contract]
    B --> C[Collect evidence on amendment]
    C --> D[Settler: PASS]
    D --> E[New CONFIDENCE-CONTRACT.md<br/>digest updated]
    E --> F[Prior version still<br/>addressable]
    F --> G[Future cycles use<br/>new contract]
```

**Outcome:** Process improved via settled amendment. History preserved.  
**Efficiency metric candidate:** Number of settled amendments that reduce future CONFLICT or INDETERMINATE rate.

---

## 7. Self-Adjustment Hold / Quarantine Path

```mermaid
flowchart TD
    A[LearningEvent] --> B[AmendmentProposal]
    B --> C[Evidence mixed or missing]
    C --> D[Settlement CONFLICT<br/>or INDETERMINATE]
    D --> E[Quarantine amendment]
    E --> F[Process unchanged]
    F --> G[Prior definition<br/>remains canonical]
```

**Outcome:** No mutation. Unresolved proposal isolated.  
**Efficiency note:** Prevents thrashing from low-evidence amendments.

---

## 8. Gate Progression Flow

```mermaid
stateDiagram-v2
    [*] --> Gate0
    Gate0 --> Gate1: structure consistent
    Gate1 --> Gate2: BRD/FRD/PRD consistent
    Gate2 --> Gate3: ADRs present
    Gate3 --> Gate4: receipts from loop
    Gate4 --> GateN: LearningEvent reviewed
    Gate3 --> Gate3: INDETERMINATE<br/>hold + more evidence
    Gate4 --> Gate4: amendment quarantined
    GateN --> [*]
```

---

## 9. Efficiency Metrics (structural candidates)

These are measurable from receipts. They are not settled success criteria.

| Metric | Definition | Desired direction | Source |
|--------|------------|-------------------|--------|
| Explicit yield | explicit observations / total observations | Higher (for informative claims) | SettlementReceipt |
| Conflict rate | CONFLICT settlements / total settlements | Lower over time (via amendments) | SettlementReceipt |
| Mismatch rate | LearningEvents / provisional answers | Lower after process amendments | LearningEvent |
| Hold duration | cycles spent in INDETERMINATE before PASS/FAIL | Lower | OrchestrationReceipt |
| Amendment success | settled PASS amendments / proposals | Context-dependent | Amendment settlement |
| Recoverability | prior digests still resolvable | 100% | Content-addressed store |
| Stub-to-extension | Gate 3 passed with stubs only | Yes for early gates | GATE-3 checklist |

Metrics themselves may become claims and be settled or quarantined.

---

## 10. Concrete End-to-End Example (Stub)

1. Claim: “30 stub nodes suffice for Gate 3 structural evidence.”
2. Run `python3 sketch.py` (64 nodes).
3. Observe ~8 PASS, ~4 FAIL → Settlement CONFLICT.
4. LearningEvent emitted (provisional may have been PASS or null).
5. AmendmentProposal: “Raise Gate 3 explicit-yield minimum or add conflict tolerance note.”
6. Amendment settled INDETERMINATE (no further evidence) → quarantined.
7. Gate 3 held. Process definition unchanged. All receipts addressable.

This demonstrates the full lifecycle without any production components.

---

**Disposition:** Visual and scenario structure only. Paths shown are illustrative. Actual settlement depends solely on explicit evidence.
