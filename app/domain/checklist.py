"""DCA-011: program-specific document checklist."""
from datetime import date

ADULT_AGE = 18  # "everybody in the household over eighteen" (00:07:33) — 18+ treated as adult


def age_on(dob: date, on: date) -> int:
    return on.year - dob.year - ((on.month, on.day) < (dob.month, dob.day))


def build_checklist(requirements: list[dict], members: list[dict], received: date,
                    emergency: bool = False) -> list[dict]:
    """Expand active requirements for one program into checklist lines.

    requirements: {id, label, applies_to, condition}
    members: {person_id, first_name, last_name, dob (date), relationship}; applicant first.
    """
    applicant = next(m for m in members if m["relationship"] == "applicant")
    adults = [m for m in members if age_on(m["dob"], received) >= ADULT_AGE]
    children = [m for m in members if age_on(m["dob"], received) < ADULT_AGE]
    lines = []
    for r in requirements:
        if r.get("condition") == "emergency" and not emergency:
            continue
        targets = {"applicant": [applicant], "household": [None],
                   "each_adult": adults, "each_child": children}[r["applies_to"]]
        for m in targets:
            label = r["label"] if m is None else f"{r['label']} — {m['first_name']} {m['last_name']}"
            lines.append({"requirement_id": r["id"], "person_id": m and m["person_id"], "label": label})
    return lines
