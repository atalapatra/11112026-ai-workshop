"""DCA-004: Record a new application at intake."""
import pytest

from app import db
from tests.conftest import PAT, as_user, application_form


def post(client, **kw):
    return client.post("/applications", data=application_form(**kw), follow_redirects=False)


@pytest.mark.story("DCA-004", 1)
def test_captures_members_income_address_and_program(client, conn):
    r = post(client, program="child_care", address="77 Elm Court", city="Riverton", zip="40220", members=[
        dict(first_name="Lan", last_name="Nguyen", dob="1992-12-01", relationship="applicant", monthly_income="2400"),
        dict(first_name="Bao", last_name="Nguyen", dob="2021-03-08", relationship="child", monthly_income=""),
    ])
    assert r.status_code == 303
    app = db.get_application(conn, int(r.headers["location"].rsplit("/", 1)[1]))
    assert app["program"] == "child_care"
    assert (app["household"]["address"], app["household"]["city"], app["household"]["zip"]) == \
        ("77 Elm Court", "Riverton", "40220")
    members = {m["first_name"]: m for m in app["members"]}
    assert members["Lan"]["relationship"] == "applicant" and members["Lan"]["monthly_income"] == 2400
    assert members["Bao"]["relationship"] == "child" and members["Bao"]["monthly_income"] == 0


@pytest.mark.story("DCA-004", 1)
@pytest.mark.parametrize("override, message", [
    ({"program": ""}, "Choose a program"),
    ({"address": ""}, "Address, city and ZIP are required"),
    ({"members": [dict(first_name="", last_name="", dob="", relationship="applicant")]}, "applicant"),
    ({"members": [dict(first_name="A", last_name="B", dob="1990-01-01", relationship="applicant",
                       monthly_income="-5")]}, "monthly income"),
])
def test_rejects_incomplete_applications(client, conn, override, message):
    r = post(client, **override)
    assert r.status_code == 422 and message in r.text
    assert conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0] == 0


@pytest.mark.story("DCA-004", 1)
def test_program_admin_cannot_record_applications(app):
    assert as_user(app, PAT).post("/applications", data=application_form()).status_code == 403


@pytest.mark.story("DCA-004", 2)
@pytest.mark.parametrize("channel", list(db.CHANNELS))
def test_captures_arrival_channel(client, conn, channel):
    assert post(client, channel=channel).status_code == 303
    assert conn.execute("SELECT channel FROM applications").fetchone()[0] == channel


@pytest.mark.story("DCA-004", 2)
def test_unknown_channel_rejected(client):
    assert post(client, channel="carrier_pigeon").status_code == 422


@pytest.mark.story("DCA-004", 3)
def test_captures_received_date_and_starts_clock(client, conn):
    assert post(client, received_date="2026-11-02").status_code == 303
    row = conn.execute("SELECT received_date, due_date FROM applications").fetchone()
    assert row["received_date"] == "2026-11-02" and row["due_date"] == "2026-12-02"


@pytest.mark.story("DCA-004", 3)
def test_received_date_cannot_be_in_future(client):
    r = post(client, received_date="2026-11-12")
    assert r.status_code == 422 and "future" in r.text


@pytest.mark.story("DCA-004", 3)
def test_existing_person_from_search_is_reused_not_duplicated(client, conn):
    post(client)
    pid = conn.execute("SELECT id FROM persons").fetchone()[0]
    page = client.get(f"/applications/new?person_id={pid}")
    assert 'value="Reyes"' in page.text
    r = post(client, program="utility", members=[dict(person_id=str(pid), relationship="applicant")])
    assert r.status_code == 303
    assert conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0] == 1
