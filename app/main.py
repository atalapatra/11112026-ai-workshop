"""FastAPI app factory. Run: .venv/bin/uvicorn app.main:app --reload"""
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import db
from app.web import admin, cases, intake, queue, search, session

STATIC = Path(__file__).with_name("static")


def create_app(db_path: str | None = None) -> FastAPI:
    app = FastAPI(title="DCA Case Management — Slice 1")
    app.state.conn = db.connect(db_path or os.environ.get("DCA_DB", "dca.db"))
    db.init_db(app.state.conn)
    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    for module in (session, queue, search, intake, cases, admin):
        app.include_router(module.router)
    return app


app = create_app() if os.environ.get("DCA_NO_AUTOAPP") != "1" else None
