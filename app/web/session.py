"""Stub for DCA-045 (SSO) / DCA-047 (roles): pick a seeded user; stored in a cookie.
Also the shared render() helper every route module uses."""
from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app import clock, db

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")
templates.env.globals.update(PROGRAMS=db.PROGRAMS, CHANNELS=db.CHANNELS, APPLIES_TO=db.APPLIES_TO,
                             RELATIONSHIPS=db.RELATIONSHIPS)
DEFAULT_USER = 2
COOKIE = "dca_user"


def conn(request: Request):
    return request.app.state.conn


def current_user(request: Request) -> dict:
    try:
        uid = int(request.cookies.get(COOKIE, DEFAULT_USER))
    except ValueError:
        uid = DEFAULT_USER
    return db.get_user(conn(request), uid) or db.get_user(conn(request), DEFAULT_USER)


def require_role(request: Request, *roles) -> dict:
    user = current_user(request)
    if user["role"] not in roles:
        raise HTTPException(403, f"Requires role: {', '.join(roles)}")
    return user


def render(request: Request, template: str, status_code: int = 200, **ctx):
    user = current_user(request)
    c = conn(request)
    return templates.TemplateResponse(request, template, status_code=status_code, context={
        "user": user, "users": db.users(c), "unread": db.unread_count(c, user["id"]),
        "today": clock.today(), **ctx})


@router.post("/session")
def switch_user(user_id: int = Form(...), next: str = Form("/")):
    resp = RedirectResponse(next if next.startswith("/") else "/", status_code=303)
    resp.set_cookie(COOKIE, str(user_id), httponly=True, samesite="lax")
    return resp


@router.get("/notifications")
def notifications(request: Request):
    user = current_user(request)
    items = db.notifications(conn(request), user["id"])
    resp = render(request, "notifications.html", items=items)
    db.mark_notifications_read(conn(request), user["id"])
    return resp
