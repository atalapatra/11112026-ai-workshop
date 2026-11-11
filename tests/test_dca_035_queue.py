"""DCA-035: Expedited cases go to the top and alert prominently."""
import re

import pytest

from app import db
from app.domain import deadlines
from tests.conftest import ANDRE, MARCUS, TERESA, as_user, create


def queue_ids(html):
    return [int(x) for x in re.findall(r'data-app-id="(\d+)"', html)]


@pytest.mark.story("DCA-035", 1)
def test_queue_order_rule():
    apps = [dict(id=1, expedited=False, due_date="2026-11-12"),
            dict(id=2, expedited=True, due_date="2026-11-16"),
            dict(id=3, expedited=False, due_date="2026-11-11"),
            dict(id=4, expedited=True, due_date="2026-11-13")]
    assert [a["id"] for a in deadlines.queue_order(apps)] == [4, 2, 3, 1]


@pytest.mark.story("DCA-035", 1)
def test_expedited_case_sorts_above_older_regular_cases(client, conn):
    old = create(conn, program="utility", received_date="2026-10-15")       # due 11-14, very close
    exp = create(conn, received_date="2026-11-11", eviction_date="2026-11-15")  # expedited, due 11-16
    mid = create(conn, program="child_care", received_date="2026-11-01")
    assert queue_ids(client.get("/").text) == [exp, old, mid]


@pytest.mark.story("DCA-035", 1)
def test_supervisor_queue_includes_team_with_expedited_first(app, conn):
    a = create(conn, user_id=TERESA, program="utility", received_date="2026-10-20")
    b = create(conn, user_id=ANDRE, received_date="2026-11-11", eviction_date="2026-11-12")
    assert queue_ids(as_user(app, MARCUS).get("/").text) == [b, a]
    assert queue_ids(as_user(app, TERESA).get("/").text) == [a]  # caseworkers see only their own


@pytest.mark.story("DCA-035", 2)
def test_expedited_rows_are_visually_distinct_with_text_label(client, conn):
    create(conn, received_date="2026-11-11", eviction_date="2026-11-12")
    html = client.get("/").text
    assert 'class="expedited"' in html
    assert "EXPEDITED</span>" in html  # not colour alone (Section 508)


@pytest.mark.story("DCA-035", 2)
def test_expedited_notifies_caseworker_and_supervisor(app, conn):
    app_id = create(conn, user_id=TERESA, received_date="2026-11-11", eviction_date="2026-11-12")
    for uid in (TERESA, MARCUS):
        notes = db.notifications(conn, uid)
        assert len(notes) == 1 and notes[0]["application_id"] == app_id
        assert notes[0]["message"].startswith("EXPEDITED")
    assert db.notifications(conn, ANDRE) == []
    assert 'aria-label="1 unread"' in as_user(app, MARCUS).get("/").text


@pytest.mark.story("DCA-035", 2)
def test_regular_case_does_not_notify(conn):
    create(conn, received_date="2026-11-11", eviction_date="2026-12-30")
    assert db.notifications(conn, TERESA) == [] and db.notifications(conn, MARCUS) == []
