
import math


VALID_EVIDENCE_STATUSES = {
    "SUPPORTED",
    "CONTRADICTED",
    "NOT_VERIFIED",
}

VALID_DECISIONS = {"ALLOW", "REVIEW", "BLOCK"}


def classify_confidence(confidence):
    if (
        isinstance(confidence, bool)
        or not isinstance(confidence, (int, float))
        or not math.isfinite(confidence)
        or not 0 <= confidence <= 1
    ):
        raise ValueError(
            "Confidence must be a finite number between 0 and 1."
        )

    if confidence >= 0.8:
        return "HIGH"
    elif confidence >= 0.5:
        return "MEDIUM"
    return "LOW"


def make_decision(confidence, evidence_status):
    trust_level = classify_confidence(confidence)

    if evidence_status not in VALID_EVIDENCE_STATUSES:
        decision = "REVIEW"
    elif evidence_status == "CONTRADICTED":
        decision = "BLOCK"
    elif evidence_status == "NOT_VERIFIED":
        decision = "REVIEW"
    elif trust_level == "HIGH":
        decision = "ALLOW"
    elif trust_level == "MEDIUM":
        decision = "REVIEW"
    else:
        decision = "BLOCK"

    return {
        "trust_level": trust_level,
        "decision": decision,
    }


def make_final_decision(
    confidence,
    evidence_status,
    authorized,
    risk_score,
):
    """Apply answer trust, authorization, and risk rules."""

    if not isinstance(authorized, bool):
        raise ValueError("Authorization must be a boolean.")

    if (
        isinstance(risk_score, bool)
        or not isinstance(risk_score, (int, float))
        or not math.isfinite(risk_score)
        or not 0 <= risk_score <= 100
    ):
        raise ValueError("Risk score must be between 0 and 100.")

    result = make_decision(confidence, evidence_status)

    # Safety rules take priority over answer trust.
    if not authorized:
        final_decision = "BLOCK"
        final_reason = "The proposed action is not authorized."
    elif risk_score >= 80:
        final_decision = "BLOCK"
        final_reason = "The action exceeds the configured risk threshold."
    elif result["decision"] == "BLOCK":
        final_decision = "BLOCK"
        final_reason = (
            "The answer is contradicted by evidence "
            "or has insufficient confidence."
        )
    elif result["decision"] == "REVIEW":
        final_decision = "REVIEW"
        final_reason = (
            "The answer needs stronger evidence "
            "or additional review."
        )
    else:
        final_decision = "ALLOW"
        final_reason = (
            "The configured answer, authorization, "
            "and risk checks passed."
        )

    return {
        "trust_level": result["trust_level"],
        "answer_decision": result["decision"],
        "final_decision": final_decision,
        "final_reason": final_reason,
    }
