"""DCA-004: record a new application (also triggers DCA-011 checklist and DCA-034 expedited flag)."""
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app import clock, db
from app.web.session import conn, current_user, render, require_role

router = APIRouter()
MEMBER_ROWS = 6
MEMBER_FIELDS = ("person_id", "first_name", "last_name", "dob", "ssn", "relationship", "monthly_income")


def blank_form(person=None):
    members = [{"relationship": "applicant" if i == 0 else ""} for i in range(MEMBER_ROWS)]
    if person:
        members[0].update(person_id=person["id"], first_name=person["first_name"],
                          last_name=person["last_name"], dob=person["dob"])
    return {"program": "", "channel": "", "received_date": clock.today().isoformat(), "address": "",
            "city": "", "zip": "", "eviction_date": "", "emergency": False, "members": members}


@router.get("/applications/new")
def new_application(request: Request, person_id: int | None = None):
    require_role(request, "caseworker", "supervisor")
    person = db.get_person(conn(request), person_id) if person_id else None
    return render(request, "intake.html", form=blank_form(person), error=None)


@router.post("/applications")
async def create_application(request: Request):
    user = require_role(request, "caseworker", "supervisor")
    f = await request.form()
    members = [{k: f.get(f"members-{i}-{k}", "") for k in MEMBER_FIELDS} for i in range(MEMBER_ROWS)]
    form = {k: f.get(k, "") for k in ("program", "channel", "received_date", "address", "city", "zip",
                                      "eviction_date")}
    form["emergency"] = f.get("emergency") == "on"
    try:
        app_id = db.create_application(conn(request), user_id=user["id"], members=members, **form)
    except db.ValidationError as e:
        return render(request, "intake.html", status_code=422, form={**form, "members": members},
                      error=str(e))
    return RedirectResponse(f"/applications/{app_id}", status_code=303)
