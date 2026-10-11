
# AgentTrust 🛡️
### Evidence-to-Action Auditor for AI Agents

AgentTrust is a local AI governance prototype that evaluates AI-generated answers and proposed actions before they are trusted.

It combines evidence verification, confidence thresholds, permission checks, risk scoring, and an audit trail to produce one of three outcomes:

**ALLOW · REVIEW · BLOCK**

## Problem

AI agents can produce incorrect answers or propose actions that exceed their permissions. AgentTrust demonstrates a structured way to evaluate answers and proposed actions before any external action is taken.

## Features

- **Local LLM:** Generates answers using Ollama and Llama 3.2.
- **Evidence checking:** Compares answers against a small local knowledge base.
- **Confidence classification:** Categorizes reported confidence as HIGH, MEDIUM, or LOW.
- **Permission checks:** Evaluates proposed actions against an allowlist.
- **Risk scoring:** Assigns configured risk scores to actions.
- **Decision engine:** Combines evidence, confidence, authorization, and risk rules.
- **Audit history:** Stores evaluation records in JSON Lines format.
- **Streamlit dashboard:** Displays evaluation results and recorded decisions.

## Architecture

1. User submits a question and proposed action.
2. The local model generates an answer, confidence value, and reason.
3. The knowledge base retrieves potentially relevant evidence.
4. The evidence checker evaluates the answer against supported facts.
5. The permission checker evaluates the proposed action.
6. The risk scorer assigns a configured risk score.
7. The decision engine returns ALLOW, REVIEW, or BLOCK.
8. The evaluation is written to the audit log.

## Technology Stack

- Python
- Streamlit
- Ollama
- Llama 3.2
- unittest
- JSON / JSONL

## Run Locally

### Prerequisites

- Python 3.12+
- Ollama installed
- Git

### Setup

Clone or download this repository, then open its directory in a terminal.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Download the model:

```bash
ollama pull llama3.2:3b
```

Start the dashboard:

```bash
python -m streamlit run app.py
```

Run the tests:

```bash
python -m unittest -v
```

## Safety and Limitations

- This is a prototype, not a production security boundary.
- Evidence verification currently supports a limited set of known facts; it is not a general-purpose fact verifier.
- Model-reported confidence is not a calibrated probability of correctness.
- Risk scores and permission rules are configured heuristics, not universal risk measurements.
- ALLOW means the configured checks passed; it does not guarantee that an answer or action is safe.
- Proposed actions are evaluated but not executed.
- The local dashboard requires the model and Ollama to be available on the machine running it.

## Future Improvements

- Broader evidence verification and source attribution
- Adversarial input and edge-case evaluation
- More detailed policy configuration
- Improved audit filtering and export
- Deployment architecture for a public demo

## Author

Built as an AI engineering portfolio project exploring evidence-grounded decisions, authorization, risk assessment, and AI governance.
