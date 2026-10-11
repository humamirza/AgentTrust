
def calculate_risk(action, authorized):
    risk_scores = {
        "search_knowledge": 10,
        "summarize_document": 15,
        "draft_email": 25,
        "send_email": 60,
        "delete_files": 90,
        "transfer_money": 100
    }

    risk = risk_scores.get(action, 70)

    if not authorized:
        risk = max(risk, 90)

    if risk >= 80:
        level = "HIGH"
    elif risk >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_score": risk,
        "risk_level": level
    }
