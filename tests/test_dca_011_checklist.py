"""DCA-011: Program-specific document checklist."""
import pytest

from app import db
from tests.conftest import PAT, TERESA, as_user, create


def labels(conn, app_id):
    return [c["label"] for c in db.checklist_for(conn, app_id)]


FAMILY = [
    dict(first_name="Ana", last_name="Reyes", dob="1990-05-01", relationship="applicant", monthly_income="1500"),
    dict(first_name="Rob", last_name="Reyes", dob="1988-02-02", relationship="spouse/partner", monthly_income="900"),
    dict(first_name="Eli", last_name="Reyes", dob="2008-11-11", relationship="child"),   # turns 18 on TODAY
    dict(first_name="Mia", last_name="Reyes", dob="2016-03-03", relationship="child"),
]


@pytest.mark.story("DCA-011", 1)
def test_housing_checklist_includes_income_for_every_adult(conn):
    app_id = create(conn, program="housing", members=FAMILY)
    assert labels(conn, app_id) == [
        "Photo ID — Ana Reyes",
        "Lease",
        "Eviction notice or past-due notice from landlord",
        "Proof of income — Ana Reyes",
        "Proof of income — Rob Reyes",
        "Proof of income — Eli Reyes",  # 18 on the received date counts as adult
    ]


@pytest.mark.story("DCA-011", 2)
def test_utility_checklist(conn):
    assert labels(conn, create(conn, program="utility", members=FAMILY)) == [
        "Photo ID — Ana Reyes", "Proof of income", "Utility bill"]


@pytest.mark.story("DCA-011", 2)
def test_utility_emergency_adds_shutoff_notice(conn):
    assert "Shutoff notice" in labels(conn, create(conn, program="utility", emergency=True, members=FAMILY))


@pytest.mark.story("DCA-011", 3)
def test_child_care_checklist_includes_birth_certificate_per_child(conn):
    assert labels(conn, create(conn, program="child_care", members=FAMILY)) == [
        "Proof of income", "Proof of work or school — Ana Reyes",
        "Birth certificate or equivalent — Mia Reyes"]


@pytest.mark.story("DCA-011", 4)
def test_items_can_be_checked_off_as_received(client, conn):
    app_id = create(conn, program="utility")
    item = db.checklist_for(conn, app_id)[0]
    r = client.post(f"/applications/{app_id}/checklist/{item['id']}/verify",
                    data={"document_ref": "State ID card"}, follow_redirects=True)
    assert r.status_code == 200
    assert "1/3 verified" in r.text
    assert db.checklist_for(conn, app_id)[0]["verified_at"]


@pytest.mark.story("DCA-011", 5)
def test_program_admin_adds_requirement_applied_to_new_applications(app, conn):
    before = create(conn, program="utility")
    admin = as_user(app, PAT)
    r = admin.post("/admin/requirements", data={"program": "utility", "label": "Landlord letter",
                                                "applies_to": "household", "condition": ""})
    assert r.status_code == 200 and "Landlord letter" in r.text
    after = create(conn, program="utility")
    assert "Landlord letter" in labels(conn, after)
    assert "Landlord letter" not in labels(conn, before)  # existing checklists are snapshots


@pytest.mark.story("DCA-011", 5)
def test_program_admin_deactivates_requirement(app, conn):
    req = next(r for r in db.requirements(conn, "utility") if r["label"] == "Utility bill")
    as_user(app, PAT).post(f"/admin/requirements/{req['id']}/active", data={"active": "0"})
    assert "Utility bill" not in labels(conn, create(conn, program="utility"))


@pytest.mark.story("DCA-011", 5)
def test_only_program_admin_can_change_requirements(app):
    caseworker = as_user(app, TERESA)
    assert caseworker.get("/admin/requirements").status_code == 403
    assert caseworker.post("/admin/requirements", data={"program": "utility", "label": "x",
                                                        "applies_to": "household"}).status_code == 403
