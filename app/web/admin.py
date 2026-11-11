"""DCA-011 AC5: program admin maintains required documents."""
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from app import db
from app.web.session import conn, render, require_role

router = APIRouter()


@router.get("/admin/requirements")
def list_requirements(request: Request):
    require_role(request, "program_admin")
    return render(request, "admin_requirements.html",
                  reqs=db.requirements(conn(request), active_only=False), error=None)


@router.post("/admin/requirements")
def add_requirement(request: Request, program: str = Form(""), label: str = Form(""),
                    applies_to: str = Form(""), condition: str = Form("")):
    require_role(request, "program_admin")
    try:
        db.add_requirement(conn(request), program, label, applies_to, condition or None)
    except db.ValidationError as e:
        return render(request, "admin_requirements.html", status_code=422,
                      reqs=db.requirements(conn(request), active_only=False), error=str(e))
    return RedirectResponse("/admin/requirements", status_code=303)


@router.post("/admin/requirements/{req_id}/active")
def toggle_requirement(request: Request, req_id: int, active: str = Form(...)):
    require_role(request, "program_admin")
    db.set_requirement_active(conn(request), req_id, active == "1")
    return RedirectResponse("/admin/requirements", status_code=303)
