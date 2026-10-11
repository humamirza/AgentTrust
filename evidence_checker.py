
def check_evidence(question, answer, evidence):
    """Verify supported capital-city facts using known evidence."""

    import re

    def normalize(text):
        text = text.lower().strip()
        return re.sub(r"[^\w\s]", "", text)

    question_clean = normalize(question)
    answer_clean = normalize(answer)

    capital_facts = {
        "france": "paris",
        "japan": "tokyo",
        "the united arab emirates": "abu dhabi",
        "italy": "rome",
        "germany": "berlin",
    }

    if not evidence:
        return "NOT_VERIFIED"

    expected_answer = None

    for country, capital in capital_facts.items():
        if (
            f"capital of {country}" in question_clean
            and "capital" in question_clean
        ):
            expected_answer = capital
            break

    if expected_answer is None:
        return "NOT_VERIFIED"

    evidence_text = normalize(" ".join(evidence))

    if expected_answer not in evidence_text:
        return "NOT_VERIFIED"

    if expected_answer in answer_clean:
        if answer_clean == expected_answer:
            return "SUPPORTED"
        return "CONTRADICTED"

    return "CONTRADICTED"
