"""DCA-001: person search.

Search is a POST so SSNs and other identifiers never appear in URLs, server logs or browser history.
"""
from fastapi import APIRouter, Request

from app import db
from app.web.session import conn, render

router = APIRouter()
FIELDS = ("first_name", "last_name", "dob", "ssn", "address")


@router.get("/search")
def search_form(request: Request):
    return render(request, "search.html", criteria={k: "" for k in FIELDS}, searched=False, results=[])


@router.post("/search")
async def search(request: Request):
    f = await request.form()
    criteria = {k: str(f.get(k, "")) for k in FIELDS}
    searched = any(v.strip() for v in criteria.values())
    results = db.search_people(conn(request), criteria) if searched else []
    return render(request, "search.html", criteria=criteria, searched=searched, results=results)
