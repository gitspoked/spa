# RECEIPT-SCHEMA — Canonical Receipt and LearningEvent Schemas

**Status:** Draft — Gate 3 supporting  
**Version:** 0.1.0  
**Date:** 2026-11-03  
**Authority:** None. Structure only.  
**Canonical parent:** SPEC-001  
**Related:** ADR-001, FR-002, FR-005

## 1. Design Rules

- Every receipt identity = `sha256:` + hex digest of the canonical JSON payload (sorted keys, no insignificant whitespace).
- Payloads are append-only. Mutation creates a new receipt.
- Unknown fields are preserved but ignored by settlers.
- All timestamps are ISO-8601 UTC.

## 2. ResponseReceipt

```json
{
  "receipt_id": "response:sha256:...",
  "claim_id": "claim:...",
  "node_id": "node-0042",
  "node_identity": "sha256:...",
  "observation": {
    "evidence_id": "ev:node-0042:claim:...",
    "status": "PASS|FAIL|TIMEOUT|MISSING|UNAVAILABLE|MALFORMED",
    "weight": 1.0,
    "note": "string",
    "observed_at": "2026-11-03T..."
  },
  "provisional_direction": "PASS|FAIL|null",
  "provisional_confidence": 0.0,
  "answer_permitted": false,
  "rationale": "string",
  "created_at": "2026-11-03T..."
}
```

## 3. SettlementReceipt

```json
{
  "receipt_id": "settlement:sha256:...",
  "claim_id": "claim:...",
  "state": "INDETERMINATE|PASS|FAIL|CONFLICT",
  "explicit_pass_count": 0,
  "explicit_fail_count": 0,
  "positive_sources": ["node-..."],
  "negative_sources": ["node-..."],
  "missing_required_sources": [],
  "evidence_ids": ["ev:..."],
  "created_at": "2026-11-03T..."
}
```

## 4. LearningEvent

```json
{
  "event_id": "learning:sha256:...",
  "response_receipt_id": "response:sha256:...",
  "settlement_receipt_id": "settlement:sha256:...",
  "provisional_direction": "PASS|FAIL|null",
  "provisional_confidence": 0.0,
  "settled_state": "INDETERMINATE|PASS|FAIL|CONFLICT",
  "mismatch": true,
  "rationale": "string",
  "created_at": "2026-11-03T..."
}
```

## 5. AmendmentProposal (extends Claim)

```json
{
  "claim_id": "amend:gate-3-criteria:001",
  "text": "Relax Gate 3 minimum node count from 30 to 10 for stub demonstrations",
  "triggered_by_learning_event": "learning:sha256:...",
  "proposed_change": {
    "target": "docs/GATES.md#Gate-3",
    "diff_summary": "..."
  },
  "created_at": "2026-11-03T..."
}
```

Settlement of an AmendmentProposal follows the normal four-state rules.

## 6. Canonical Serialization

```python
import json, hashlib
def receipt_id(kind: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return f"{kind}:sha256:{hashlib.sha256(raw).hexdigest()}"
```

## 8. Optional Inner Fields (ADR-006)

ResponseReceipt and SettlementReceipt may include:
```json
"inner_digests": ["sha256:…", "sha256:…"]
```

LearningEvent may include:
```json
"inner_digest_changes": [
  {"path": "spines/document.md", "old": "sha256:…", "new": "sha256:…"}
]
```

Gate3Evidence may include:
```json
"manifest_digest": "sha256:…"
```

These fields are optional. Their absence is valid. Malformed values produce a MALFORMED observation and do not settle the parent claim.

---

**Disposition:** Structural schema. Subject to amendment via settled LearningEvent if field requirements prove insufficient.
