# AMENDMENT-TEMPLATE — LearningEvent to AmendmentProposal

**Status:** Draft  
**Version:** 0.1.0  
**Date:** 2026-11-03  
**Authority:** None.  
**Canonical parent:** SPEC-001  
**Related:** PROCESS §5, RECEIPT-SCHEMA.md AmendmentProposal, ADR-003

## 1. Purpose

Reduce friction in the self-adjustment loop by giving the Learning Agent a concrete template.

## 2. Template

```yaml
amendment_proposal:
  claim_id: "amend:<target>:<seq>"
  text: "One-sentence description of the proposed change"
  triggered_by_learning_event: "learning:sha256:..."
  target_artifact: "docs/CONFIDENCE-CONTRACT.md"   # or GATES.md, etc.
  proposed_change:
    type: "json-patch | unified-diff | field-update"
    payload: "..."
  evidence_requested:
    - "Re-run Gate 3 harness at N=64 and N=100"
    - "Confirm explicit yield does not drop below 0.05"
  success_criterion: "Settlement of this amendment is PASS and subsequent Gate 3 runs show lower mismatch_rate"
  created_at: "ISO-8601"
```

## 3. Settlement

The filled template becomes a normal Claim and is settled with the four-state rules. Only PASS may update the target artifact (producing a new digest).

## 4. Example (confidence contract tightening)

```yaml
text: "Raise min_confidence from 0.70 to 0.85 after observing high mismatch_rate"
target_artifact: "docs/CONFIDENCE-CONTRACT.md"
proposed_change:
  type: "field-update"
  payload: {"min_confidence": 0.85}
success_criterion: "Next 3 Gate 3 runs show mismatch_rate < 0.2"
```

---

**Disposition:** Structural template. Use does not guarantee acceptance.
