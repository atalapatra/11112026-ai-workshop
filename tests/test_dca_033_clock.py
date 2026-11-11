"""DCA-033: Track the 30-day processing clock on every application."""
from datetime import date

import pytest

from app import clock, db
from app.domain import deadlines
from tests.conftest import TERESA, create


@pytest.mark.story("DCA-033", 1)
@pytest.mark.parametrize("program", ["housing", "utility", "child_care"])
def test_clock_is_30_days_from_received_for_every_program(conn, program):
    app_id = create(conn, program=program, received_date="2026-11-02")
    assert db.get_application(conn, app_id)["due_date"] == "2026-12-02"


@pytest.mark.story("DCA-033", 1)
def test_clock_starts_on_received_date_not_entry_date(conn):
    app_id = create(conn, received_date="2026-10-20")  # mailed in, keyed later
    app = db.get_application(conn, app_id)
    assert app["due_date"] == "2026-11-19" and app["days_elapsed"] == 22


@pytest.mark.story("DCA-033", 2)
def test_outstanding_documents_do_not_pause_clock(conn):
    app_id = create(conn, received_date="2026-11-01")
    assert all(not c["verified_at"] for c in db.checklist_for(conn, app_id))  # still waiting on everything
    clock.set_today(date(2026, 11, 21))
    assert db.get_application(conn, app_id)["days_remaining"] == 10


@pytest.mark.story("DCA-033", 2)
def test_days_remaining_depends_only_on_due_date():
    assert deadlines.days_remaining(date(2026, 12, 1), date(2026, 11, 11)) == 20
    assert deadlines.days_remaining(date(2026, 11, 1), date(2026, 11, 11)) == -10


@pytest.mark.story("DCA-033", 3)
def test_days_remaining_shown_in_queue_and_on_case(client, conn):
    app_id = create(conn, received_date="2026-11-01")  # due 12-01, 20 days left
    queue = client.get("/").text
    assert f'data-app-id="{app_id}"' in queue and '<td class="days">20</td>' in queue
    case = client.get(f"/applications/{app_id}").text
    assert '<span class="v" id="days-remaining">20</span>' in case


@pytest.mark.story("DCA-033", 3)
def test_overdue_shown_as_overdue(client, conn):
    create(conn, received_date="2026-10-01")  # due 10-31
    assert "11 overdue" in client.get("/").text
