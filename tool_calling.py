CHECK_LIST = {
    "weather": {
        "question": "What is the weather outside?",
        "answer": None
    },
    "headache": {
        "question": "Do you have a headache?",
        "answer": None
    }
}

TOOLS = [{
    "function_declarations": [{
        "name": "record_answers",
        "description": "Record the user's answers to weather and headache.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "weather": {
                    "type": "STRING",
                    "description": "Current weather outside (e.g., sunny, rainy, cloudy)"
                },
                "headache": {
                    "type": "STRING",
                    "description": "Whether the user has a headache",
                    "enum": ["yes", "no"]
                }
            },
            "required": []  # båda är valfria; fyll i när användaren nämner något
        }
    }]
}]


def is_checklist_complete(cl) -> bool:
    return all(item["answer"] is not None for item in cl.values())


def update_checklist(cl, answers: dict):
    updated = []
    for k, v in answers.items():
        if k in cl and v is not None and cl[k]["answer"] is None:
            cl[k]["answer"] = v
            updated.append(k)
    return updated


def record_answers(checklist: dict, payload: dict) -> dict:
    """
    Lokala verktyget: uppdatera checklistan och returnera ett enkelt payload.
    """
    updated = update_checklist(checklist, payload)
    return {
        "updated_fields": updated,
        "current_state": {k: v["answer"] for k, v in checklist.items()},
        "is_complete": is_checklist_complete(checklist),
    }