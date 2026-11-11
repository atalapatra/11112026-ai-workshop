"""DCA-012: Record who verified each document and when."""
import sqlite3

import pytest

from app import db
from tests.conftest import ANDRE, as_user, create


@pytest.fixture
def item(conn):
    app_id = create(conn, program="utility")
    return app_id, db.checklist_for(conn, app_id)[0]["id"]


@pytest.mark.story("DCA-012", 1)
def test_verification_records_user_timestamp_and_document(app, conn, item):
    app_id, item_id = item
    as_user(app, ANDRE).post(f"/applications/{app_id}/checklist/{item_id}/verify",
                             data={"document_ref": "Driver's license exp 2029"})
    row = db.checklist_for(conn, app_id)[0]
    assert row["verified_by"] == ANDRE and row["verified_by_name"] == "Andre Wilson"
    assert row["verified_at"].startswith("20")
    assert row["document_ref"] == "Driver's license exp 2029"


@pytest.mark.story("DCA-012", 1)
def test_verification_requires_document_description(client, conn, item):
    app_id, item_id = item
    r = client.post(f"/applications/{app_id}/checklist/{item_id}/verify", data={"document_ref": "  "})
    assert r.status_code == 422 and "Describe the document" in r.text
    assert db.checklist_for(conn, app_id)[0]["verified_at"] is None


@pytest.mark.story("DCA-012", 2)
def test_verification_history_is_visible_on_case(client, conn, item):
    app_id, item_id = item
    client.post(f"/applications/{app_id}/checklist/{item_id}/verify", data={"document_ref": "State ID"})
    page = client.get(f"/applications/{app_id}").text
    assert "Verified by <b>Teresa Alvarez</b>" in page and "State ID" in page


@pytest.mark.story("DCA-012", 2)
def test_verification_cannot_be_changed_through_the_app(client, conn, item):
    app_id, item_id = item
    url = f"/applications/{app_id}/checklist/{item_id}/verify"
    client.post(url, data={"document_ref": "State ID"})
    assert client.post(url, data={"document_ref": "Something else"}).status_code == 409
    assert db.checklist_for(conn, app_id)[0]["document_ref"] == "State ID"


@pytest.mark.story("DCA-012", 2)
def test_verification_cannot_be_changed_in_the_database(client, conn, item):
    app_id, item_id = item
    client.post(f"/applications/{app_id}/checklist/{item_id}/verify", data={"document_ref": "State ID"})
    with pytest.raises(sqlite3.IntegrityError, match="immutable"):
        conn.execute("UPDATE verifications SET document_ref = 'x'")
    with pytest.raises(sqlite3.IntegrityError, match="immutable"):
        conn.execute("DELETE FROM verifications")
