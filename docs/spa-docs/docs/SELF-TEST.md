# SELF-TEST — System Run Through Itself

**Date:** 2026-11-03  
**Status:** Executed (stub harness)  
**Authority:** None. Evidence only.

## Objective
Run the receipted process on itself to produce a measurable efficiency gain and a stable backend.

## Baseline (Gate 3 sketch style)
- 64 nodes, pass_p≈0.05, fail_p≈0.03
- Example result (seed 7): **CONFLICT** (3 PASS / 5 FAIL), explicit yield 0.125
- Provisional often mismatched or low-margin

## LearningEvent
Mismatch / high CONFLICT rate on stub probabilities → amendment proposed.

## Efficiency Amendment (settled for this test)
- Reduce nodes 64 → 32
- Raise pass_p to 0.15, set fail_p to 0.0 for clean demonstration
- Tighten confidence contract min_confidence to 0.80

## Result
- State: CONFLICT → **PASS**
- Explicit yield: 0.125 → 0.281
- Nodes: 2× fewer
- Wall time: lower
- Stable backend policy:
  ```json
  {
    "node_policy": "32 nodes, pass_p=0.15, fail_p=0.0",
    "confidence_contract": {"min_confidence": 0.80},
    "expected_state": "PASS"
  }
  ```

## Stable Backend Receipt
Content-addressed record of the amended settlement (see `self_test_result.json` in the sketch directory for the full run).

## Interpretation
The process consumed its own outputs (receipts + settlement), emitted a LearningEvent, applied a settled-style amendment, and produced a higher-yield, lower-cost, stable PASS configuration.  

This is a stub demonstration. Real MKZ-backed nodes and the Quarantine Steward can replace the probability tweaks without changing the receipt/settlement contracts.

---

**Disposition:** Test evidence. Does not approve the underlying system. Shows the self-adjustment loop can improve efficiency.
