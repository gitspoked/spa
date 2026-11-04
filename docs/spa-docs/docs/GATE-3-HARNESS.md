# GATE-3-HARNESS — Executable Evidence Harness for Gate 3/4

**Status:** Draft — Gate 3 extension  
**Version:** 0.1.0  
**Date:** 2026-11-03  
**Authority:** None. Structure only.  
**Canonical parent:** SPEC-001  
**Related:** GATE-3-ORCHESTRATION-LOOP.md, RECEIPT-SCHEMA.md, VISUAL-FLOWS.md metrics

## 1. Purpose

Turn Gate 3 from a manual sketch run into a repeatable, receipt-producing harness that also emits the efficiency metrics required for Gate 4.

The harness remains stub-based. It does not require LangGraph, containers, or external storage.

## 2. Inputs

- `claim`: Claim object
- `num_nodes`: int (default 64; support 30 / 100 / 300 for scale probe)
- `confidence_contract`: optional ConfidenceContract (defaults to CONFIDENCE-CONTRACT.md stub values)
- `seed`: optional int for reproducibility

## 3. Outputs (all content-addressed)

| Artifact | Kind | Required |
|----------|------|----------|
| ResponseReceipt × N | response | yes |
| SettlementReceipt | settlement | yes |
| LearningEvent | learning | if mismatch |
| Gate3Evidence | gate-evidence | yes |
| MetricsReceipt | metrics | yes |

## 4. Gate3Evidence Payload

```json
{
  "claim_id": "...",
  "num_nodes": 64,
  "explicit_pass": 0,
  "explicit_fail": 0,
  "explicit_yield": 0.0,
  "settlement_state": "CONFLICT",
  "provisional_direction": null,
  "mismatch": true,
  "wall_time_ms": 0,
  "scale_probe": false
}
```

## 5. MetricsReceipt Payload

```json
{
  "explicit_yield": 0.0,
  "conflict_rate": 0.0,
  "mismatch_rate": 0.0,
  "hold_recommended": true,
  "notes": "string"
}
```

These metrics are observations. They do not settle any claim by themselves.

## 6. Scale Probe Mode

When `scale_probe=true`, the harness runs the same claim at 30, 100, and 300 nodes and emits one MetricsReceipt per size plus a summary LearningEvent if the settlement state changes with N.

## 7. Success Criteria for Gate 3 (structural)

- Gate3Evidence receipt exists
- SettlementReceipt exists
- All receipts validate against RECEIPT-SCHEMA.md
- MetricsReceipt exists

Satisfaction of these criteria is evidence for the Gate 3 claim; it is not approval.

## 8. Implementation Note

A reference implementation may be added beside the existing sketch as `harness.py`. It must import only from the local `sies` package and the standard library.

---

**Disposition:** Structural specification of the harness. Execution produces evidence; evidence does not constitute approval.
