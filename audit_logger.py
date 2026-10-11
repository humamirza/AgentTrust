
import json
from datetime import datetime


def log_decision(record):
    record["timestamp"] = datetime.now().astimezone().isoformat()

    with open("audit_log.jsonl", "a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")

    print("Audit log saved successfully.")
