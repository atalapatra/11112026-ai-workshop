"""Case view: clock (DCA-033/034), checklist (DCA-011) and verification (DCA-012)."""
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from app import db
from app.web.session import conn, render, require_role

router = APIRouter()


@router.get("/applications/{app_id}")
def view_application(request: Request, app_id: int, error: str | None = None):
    app = db.get_application(conn(request), app_id)
    if not app:
        raise HTTPException(404, "Application not found")
    return render(request, "case.html", app=app, error=error)


@router.post("/applications/{app_id}/checklist/{item_id}/verify")
def verify(request: Request, app_id: int, item_id: int, document_ref: str = Form("")):
    user = require_role(request, "caseworker", "supervisor")
    try:
        db.verify_item(conn(request), app_id, item_id, user["id"], document_ref)
    except db.AlreadyVerified as e:
        raise HTTPException(409, str(e))
    except LookupError as e:
        raise HTTPException(404, str(e))
    except db.ValidationError as e:
        app = db.get_application(conn(request), app_id)
        return render(request, "case.html", status_code=422, app=app, error=str(e), error_item=item_id)
    return RedirectResponse(f"/applications/{app_id}#item-{item_id}", status_code=303)
