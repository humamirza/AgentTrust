import ollama
import json
from trust_engine import make_decision
from knowledge_base import search_knowledge
from permission_checker import check_permission
from risk_scorer import calculate_risk
from audit_logger import log_decision

user_question = input("What do you want to ask the AI? ")

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "system",
            "content": """
You are a careful and honest AI assistant.

Return your response ONLY as valid JSON with exactly these three fields:
- answer: your answer to the user's question
- confidence: a number between 0 and 1
- reason: a short explanation of why you have that level of confidence

Do not write anything outside the JSON.
"""
        },
        {
            "role": "user",
            "content": user_question
        }
    ]
)

ai_response = response["message"]["content"]

data = json.loads(ai_response)

print("\nAI response:")
print("Answer:", data["answer"])
print("Confidence:", data["confidence"])
print("Reason:", data["reason"])


# Search our local knowledge base
evidence = search_knowledge(user_question)

print("Retrieved evidence:", evidence)


if not evidence:
    evidence_status = "NOT_VERIFIED"
else:
    answer = data["answer"].strip().lower()

    evidence_text = " ".join(evidence).lower()

    # Check whether the answer appears in the retrieved evidence
    if answer and answer in evidence_text:
        evidence_status = "SUPPORTED"
    else:
        evidence_status = "NOT_VERIFIED"

print("Evidence status:", evidence_status)

# Ask the trust engine for the final decision
result = make_decision(
    data["confidence"],
    evidence_status
)

print("Trust level:", result["trust_level"])
print("Final AgentTrust decision:", result["decision"])


print("\n--- Agent Action Permission Test ---")

proposed_action = input(
    "Proposed action (e.g. draft_email or delete_files): "
).strip()

permission = check_permission(proposed_action)

print("Authorized:", permission["authorized"])
print("Permission reason:", permission["reason"])

risk_result = calculate_risk(
    proposed_action,
    permission["authorized"]
)

print("Risk score:", risk_result["risk_score"], "/ 100")
print("Risk level:", risk_result["risk_level"])


# Record the complete decision for later review
audit_record = {
    "question": user_question,
    "ai_answer": data["answer"],
    "ai_confidence": data["confidence"],
    "evidence": evidence,
    "evidence_status": evidence_status,
    "trust_level": result["trust_level"],
    "final_decision": result["decision"],
    "proposed_action": proposed_action,
    "authorized": permission["authorized"],
    "permission_reason": permission["reason"],
    "risk_score": risk_result["risk_score"],
    "risk_level": risk_result["risk_level"]
}

log_decision(audit_record)


if not permission["authorized"]:
    print("Action decision: BLOCK")
else:
    print("Action decision: ALLOW")


