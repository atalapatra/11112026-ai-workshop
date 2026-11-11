"""DCA-034: Automatically flag expedited Housing cases."""
from datetime import date

import pytest

from app import db
from app.domain import deadlines
from tests.conftest import application_form, create

R = date(2026, 11, 2)  # Monday


@pytest.mark.story("DCA-034", 1)
@pytest.mark.parametrize("eviction, expected", [
    (date(2026, 11, 2), True),    # same day
    (date(2026, 11, 9), True),    # exactly 7 days
    (date(2026, 11, 10), False),  # 8 days
    (date(2026, 10, 30), True),   # already passed at intake
    (None, False),
])
def test_eviction_within_7_days_is_expedited(eviction, expected):
    assert deadlines.is_expedited("housing", R, eviction) is expected


@pytest.mark.story("DCA-034", 1)
@pytest.mark.parametrize("program", ["utility", "child_care"])
def test_only_housing_is_expedited(program):
    assert deadlines.is_expedited(program, R, R) is False


@pytest.mark.story("DCA-034", 1)
def test_intake_sets_expedited_flag(conn):
    app_id = create(conn, received_date="2026-11-10", eviction_date="2026-11-14")
    assert db.get_application(conn, app_id)["expedited"] is True


@pytest.mark.story("DCA-034", 2)
def test_expedited_due_three_business_days_skipping_weekend():
    assert deadlines.due_date("housing", date(2026, 11, 5), date(2026, 11, 8), set()) == date(2026, 11, 10)


@pytest.mark.story("DCA-034", 2)
def test_expedited_due_date_skips_seeded_holiday(conn):
    # Received Tue 11/10; Wed 11/11 is Veterans Day -> Thu, Fri, Mon = 11/16
    app_id = create(conn, received_date="2026-11-10", eviction_date="2026-11-13")
    assert db.get_application(conn, app_id)["due_date"] == "2026-11-16"


@pytest.mark.story("DCA-034", 2)
def test_thanksgiving_week():
    holidays = {date(2026, 11, 26)}
    assert deadlines.add_business_days(date(2026, 11, 24), 3, holidays) == date(2026, 11, 30)


@pytest.mark.story("DCA-034", 3)
def test_expedited_determined_from_eviction_date_without_any_checkbox(client, conn):
    form = application_form(eviction_date="2026-11-13")
    assert not any("expedit" in k for k in form)  # the intake form has no expedited checkbox
    client.post("/applications", data=form)
    assert conn.execute("SELECT expedited FROM applications").fetchone()[0] == 1


@pytest.mark.story("DCA-034", 3)
def test_submitted_expedited_field_is_ignored(client, conn):
    client.post("/applications", data={**application_form(eviction_date="2026-12-31"), "expedited": "on"})
    assert conn.execute("SELECT expedited FROM applications").fetchone()[0] == 0
