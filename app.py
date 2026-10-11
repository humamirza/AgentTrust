
import streamlit as st
import ollama
import json
import math
from pathlib import Path


from knowledge_base import search_knowledge
from trust_engine import make_final_decision
from permission_checker import check_permission
from risk_scorer import calculate_risk
from audit_logger import log_decision
from evidence_checker import check_evidence


st.set_page_config(
    page_title="AgentTrust | AI Governance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)



st.title("🛡️ AgentTrust")
st.caption("AI AGENT GOVERNANCE  •  EVIDENCE  •  RISK  •  AUDIT")

st.markdown(
    """
    Evaluate AI-generated answers and proposed actions before trusting
    them. AgentTrust combines evidence checks, authorization rules,
    confidence thresholds, and risk scoring into an auditable decision.
    """
)

st.divider()

with st.sidebar:
    st.title("🛡️ AgentTrust")
    st.caption("Decision governance dashboard")

    st.divider()

    st.markdown("### Evaluation pipeline")
    st.markdown(
        """
        1. AI response
        2. Evidence verification
        3. Permission check
        4. Risk assessment
        5. Final decision
        """
    )

    st.divider()

    st.markdown("### About")
    st.caption(
        "A local prototype for evaluating AI answers and proposed actions. "
        "No external action is executed."
    )



question = st.text_area(
    "What should the AI evaluate?",
    placeholder="Example: What is the capital of France?"
)

action = st.selectbox(
    "Proposed action",
    [
        "search_knowledge",
        "summarize_document",
        "draft_email",
        "send_email",
        "delete_files",
        "transfer_money"
    ]
)

if st.button("Evaluate with AgentTrust", type="primary"):
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Asking the local AI and evaluating its response..."):
            try:
                response = ollama.chat(
                    model="llama3.2:3b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Answer carefully and honestly. "
                                "Return only valid JSON with exactly these fields: "
                                "answer (string), confidence (number from 0 to 1), "
                                "reason (short string). Do not add other text."
                            )
                        },
                        {"role": "user", "content": question}
                    ],
                    format="json"
                )

                



                content = response["message"]["content"]
                data = json.loads(content)

                if not isinstance(data, dict):
                    raise ValueError("AI response must be a JSON object.")

                answer = data.get("answer")
                confidence_raw = data.get("confidence")
                reason = data.get("reason")

                if not isinstance(answer, str) or not answer.strip():
                    raise ValueError("AI response must contain a non-empty answer.")

                if (
                    isinstance(confidence_raw, bool)
                    or not isinstance(confidence_raw, (int, float))
                ):
                    raise ValueError("AI confidence must be a number.")

                confidence = float(confidence_raw)

                if not math.isfinite(confidence) or not 0 <= confidence <= 1:
                    raise ValueError(
                        "AI confidence must be between 0 and 1."
                    )

                if not isinstance(reason, str) or not reason.strip():
                    raise ValueError("AI response must contain a reason.")

                answer = answer.strip()
                reason = reason.strip()



                evidence = search_knowledge(question)

                evidence_status = check_evidence(
                    question,
                    answer,
                    evidence
                )


       


                

                permission = check_permission(action)

                risk_result = calculate_risk(
                    action,
                    permission["authorized"]
                )

                result = make_final_decision(
                    confidence=confidence,
                    evidence_status=evidence_status,
                    authorized=permission["authorized"],
                    risk_score=risk_result["risk_score"],
                )

                final_decision = result["final_decision"]
                final_reason = result["final_reason"]



               

                audit_record = {
                    "question": question,
                    "ai_answer": answer,
                    "ai_confidence": confidence,
                    "ai_reason": reason,
                    "evidence": evidence,
                    "evidence_status": evidence_status,
                    "trust_level": result["trust_level"],
                    "answer_decision": result["answer_decision"],
                    "final_reason": final_reason,
                    "proposed_action": action,
                    "authorized": permission["authorized"],
                    "permission_reason": permission["reason"],
                    "risk_score": risk_result["risk_score"],
                    "risk_level": risk_result["risk_level"],
                    "final_decision": final_decision
                }

                log_decision(audit_record)


                st.divider()
                st.header("Evaluation results")

                
                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "AI confidence",
                    f"{confidence:.0%}",
                    help="Confidence reported by the local AI model; not a calibrated probability."
                )

                c2.metric(
                    "Risk score",
                    f"{risk_result['risk_score']}/100",
                    risk_result["risk_level"]
                )

                c3.metric(
                    "Evidence status",
                    evidence_status
                )


                st.subheader("AI answer")
                st.write(answer)
                st.caption(f"AI's explanation: {reason}")

                st.subheader("Retrieved evidence")
                if evidence:
                    for item in evidence:
                        st.write(f"- {item}")
                else:
                    st.info("No matching evidence was found.")

                st.subheader("Permission check")
                st.write(f"**Proposed action:** {action}")
                st.write(f"**Authorized:** {permission['authorized']}")
                st.write(permission["reason"])

                st.subheader("Final decision")
                if final_decision == "ALLOW":
                    st.success("ALLOW — the configured checks passed.")
                elif final_decision == "REVIEW":
                    st.warning("REVIEW — more evidence or human review is needed.")
                else:
                    st.error("BLOCK — the configured rules prevent this action.")

                st.caption(f"Decision rationale: {final_reason}")


                st.write(f"**Trust level:** {result['trust_level']}")
                st.write(f"**Risk level:** {risk_result['risk_level']}")

                st.caption(
                    "Prototype limitation: evidence matching uses simple text "
                    "comparison. An ALLOW decision is not a guarantee of truth "
                    "or overall safety. No external action is executed."
                )

            except Exception as error:
                st.error(f"Evaluation failed: {error}")
                st.info(
                    "Check that Ollama is running and the llama3.2:3b model "
                    "is available. No decision was recorded for this failed run."
                )

# Audit history
st.divider()
st.header("Decision audit history")

import json
from pathlib import Path

audit_file = Path("audit_log.jsonl")

if audit_file.exists():
    records = []

    with audit_file.open("r", encoding="utf-8") as file:
        for line in file:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if records:
        st.write(f"Recorded evaluations: {len(records)}")

        
        for index, record in enumerate(reversed(records), start=1):
            decision = record.get("final_decision", "Unknown")
            risk_score = record.get("risk_score", "N/A")
            evidence_status = record.get("evidence_status", "Unknown")
            question_text = record.get("question", "No question recorded")
            action_text = record.get("proposed_action", "Unknown")

            with st.expander(
                f"Evaluation {index} — {decision}"
            ):
                st.markdown(f"**Question:** {question_text}")

                col1, col2, col3 = st.columns(3)
                col1.metric("Decision", decision)
                col2.metric("Risk score", risk_score)
                col3.metric("Evidence", evidence_status)

                st.write(f"**Proposed action:** {action_text}")

                if record.get("final_reason"):
                    st.write(
                        f"**Decision rationale:** {record['final_reason']}"
                    )

                with st.expander("View full audit record"):
                    st.json(record)

    else:
        st.info("No valid audit records yet.")
else:
    st.info("No audit history yet. Run an evaluation first.")
