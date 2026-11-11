"""DCA-033 / DCA-035: work queue with deadlines, expedited first."""
from fastapi import APIRouter, Request

from app import db
from app.web.session import conn, current_user, render

router = APIRouter()


@router.get("/")
def work_queue(request: Request):
    return render(request, "queue.html", apps=db.work_queue(conn(request), current_user(request)))
