
ALLOWED_ACTIONS = {
    "search_knowledge",
    "draft_email",
    "summarize_document"
}


def check_permission(action):
    if action in ALLOWED_ACTIONS:
        return {
            "authorized": True,
            "reason": f"{action} is permitted."
        }

    return {
        "authorized": False,
        "reason": f"{action} is not permitted."
    }
