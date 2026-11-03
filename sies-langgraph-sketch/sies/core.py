from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from json import dumps
from typing import Iterable, Optional, Protocol
from datetime import datetime, timezone


class SettlementState(str, Enum):
    INDETERMINATE = "INDETERMINATE"
    PASS = "PASS"
    FAIL = "FAIL"
    CONFLICT = "CONFLICT"


class EvidenceStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    TIMEOUT = "TIMEOUT"
    MISSING = "MISSING"
    UNAVAILABLE = "UNAVAILABLE"
    MALFORMED = "MALFORMED"


class BinaryDirection(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _receipt_id(kind: str, payload: dict) -> str:
    raw = dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return f"{kind}:sha256:{sha256(raw).hexdigest()}"


@dataclass(frozen=True)
class Claim:
    claim_id: str
    text: str


@dataclass(frozen=True)
class EvidenceObservation:
    evidence_id: str
    source: str
    status: EvidenceStatus
    weight: float = 1.0
    note: str = ""
    observed_at: str = field(default_factory=_now)

    @property
    def explicit(self) -> bool:
        return self.status in {EvidenceStatus.PASS, EvidenceStatus.FAIL}


@dataclass(frozen=True)
class ConfidenceContract:
    min_confidence: float = 0.85
    min_explicit_observations: int = 1


@dataclass(frozen=True)
class SettlementPolicy:
    required_pass_sources: frozenset[str] = frozenset()


@dataclass(frozen=True)
class Prediction:
    direction: Optional[BinaryDirection]
    confidence: float
    rationale: str


class Predictor(Protocol):
    def predict(self, claim: Claim, observations: Iterable[EvidenceObservation]) -> Prediction: ...


class HeuristicPredictor:
    """Tiny stand-in for a future calibrated/GNN/ONNX predictor.

    This predictor is intentionally not settlement logic. Missing evidence contributes no sign.
    Confidence rises with signed explicit evidence weight and remains bounded below 1.0.
    """

    def predict(self, claim: Claim, observations: Iterable[EvidenceObservation]) -> Prediction:
        obs = list(observations)
        pos = sum(max(0.0, o.weight) for o in obs if o.status == EvidenceStatus.PASS)
        neg = sum(max(0.0, o.weight) for o in obs if o.status == EvidenceStatus.FAIL)
        total = pos + neg
        if total == 0:
            return Prediction(None, 0.5, "No explicit directional evidence")
        if pos == neg:
            return Prediction(None, 0.5, "Explicit evidence is balanced")
        direction = BinaryDirection.PASS if pos > neg else BinaryDirection.FAIL
        margin = abs(pos - neg) / total
        confidence = min(0.999, 0.5 + 0.5 * margin)
        return Prediction(direction, confidence, f"signed evidence margin={margin:.3f}")


@dataclass(frozen=True)
class ResponseReceipt:
    receipt_id: str
    claim_id: str
    direction: Optional[BinaryDirection]
    confidence: float
    answer_permitted: bool
    evidence_ids: tuple[str, ...]
    rationale: str
    created_at: str


@dataclass(frozen=True)
class SettlementReceipt:
    receipt_id: str
    claim_id: str
    state: SettlementState
    evidence_ids: tuple[str, ...]
    missing_required_sources: tuple[str, ...]
    positive_sources: tuple[str, ...]
    negative_sources: tuple[str, ...]
    created_at: str


@dataclass(frozen=True)
class LearningEvent:
    event_id: str
    response_receipt_id: str
    settlement_receipt_id: str
    predicted_direction: Optional[BinaryDirection]
    prediction_confidence: float
    settled_state: SettlementState
    prediction_matched: Optional[bool]
    created_at: str


class SIESEngine:
    def __init__(self, predictor: Optional[Predictor] = None):
        self.predictor = predictor or HeuristicPredictor()

    def infer(
        self,
        claim: Claim,
        observations: Iterable[EvidenceObservation],
        contract: ConfidenceContract,
    ) -> ResponseReceipt:
        obs = tuple(observations)
        prediction = self.predictor.predict(claim, obs)
        explicit_count = sum(1 for o in obs if o.explicit)
        permitted = (
            prediction.direction is not None
            and prediction.confidence >= contract.min_confidence
            and explicit_count >= contract.min_explicit_observations
        )
        payload = {
            "claim_id": claim.claim_id,
            "direction": prediction.direction.value if prediction.direction else None,
            "confidence": round(prediction.confidence, 12),
            "answer_permitted": permitted,
            "evidence_ids": [o.evidence_id for o in obs],
            "rationale": prediction.rationale,
        }
        return ResponseReceipt(
            receipt_id=_receipt_id("response", payload),
            claim_id=claim.claim_id,
            direction=prediction.direction,
            confidence=prediction.confidence,
            answer_permitted=permitted,
            evidence_ids=tuple(o.evidence_id for o in obs),
            rationale=prediction.rationale,
            created_at=_now(),
        )

    def settle(
        self,
        claim: Claim,
        observations: Iterable[EvidenceObservation],
        policy: SettlementPolicy,
    ) -> SettlementReceipt:
        obs = tuple(observations)
        positives = tuple(sorted({o.source for o in obs if o.status == EvidenceStatus.PASS}))
        negatives = tuple(sorted({o.source for o in obs if o.status == EvidenceStatus.FAIL}))
        missing = tuple(sorted(set(policy.required_pass_sources) - set(positives)))

        if positives and negatives:
            state = SettlementState.CONFLICT
        elif negatives:
            state = SettlementState.FAIL
        elif positives and not missing:
            state = SettlementState.PASS
        else:
            state = SettlementState.INDETERMINATE

        payload = {
            "claim_id": claim.claim_id,
            "state": state.value,
            "evidence_ids": [o.evidence_id for o in obs],
            "missing_required_sources": list(missing),
            "positive_sources": list(positives),
            "negative_sources": list(negatives),
        }
        return SettlementReceipt(
            receipt_id=_receipt_id("settlement", payload),
            claim_id=claim.claim_id,
            state=state,
            evidence_ids=tuple(o.evidence_id for o in obs),
            missing_required_sources=missing,
            positive_sources=positives,
            negative_sources=negatives,
            created_at=_now(),
        )

    def learning_event(
        self,
        response: ResponseReceipt,
        settlement: SettlementReceipt,
    ) -> LearningEvent:
        if response.direction is None or settlement.state in {
            SettlementState.INDETERMINATE,
            SettlementState.CONFLICT,
        }:
            matched: Optional[bool] = None
        else:
            matched = response.direction.value == settlement.state.value
        payload = {
            "response_receipt_id": response.receipt_id,
            "settlement_receipt_id": settlement.receipt_id,
            "predicted_direction": response.direction.value if response.direction else None,
            "prediction_confidence": round(response.confidence, 12),
            "settled_state": settlement.state.value,
            "prediction_matched": matched,
        }
        return LearningEvent(
            event_id=_receipt_id("learning", payload),
            response_receipt_id=response.receipt_id,
            settlement_receipt_id=settlement.receipt_id,
            predicted_direction=response.direction,
            prediction_confidence=response.confidence,
            settled_state=settlement.state,
            prediction_matched=matched,
            created_at=_now(),
        )
