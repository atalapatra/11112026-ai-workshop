import os
from datetime import date

import pytest

os.environ["DCA_NO_AUTOAPP"] = "1"  # don't create the module-level app against dca.db

from fastapi.testclient import TestClient  # noqa: E402

from app import clock, db  # noqa: E402
from app.main import create_app  # noqa: E402

TODAY = date(2026, 11, 11)  # a Wednesday, and Veterans Day (a seeded holiday)
TERESA, ANDRE, MARCUS, PAT = 2, 3, 1, 4  # caseworker, caseworker, supervisor, program admin


@pytest.fixture(autouse=True)
def fixed_today():
    clock.set_today(TODAY)
    yield
    clock.set_today(None)


@pytest.fixture
def app(tmp_path):
    return create_app(str(tmp_path / "test.db"))


@pytest.fixture
def conn(app):
    return app.state.conn


@pytest.fixture
def client(app):
    return as_user(app, TERESA)


def as_user(app, user_id):
    c = TestClient(app)
    c.cookies.set("dca_user", str(user_id))
    return c


def application_form(**overrides):
    """Form payload for POST /applications with sensible defaults (Housing, one adult)."""
    members = overrides.pop("members", [dict(first_name="Ana", last_name="Reyes", dob="1990-05-01",
                                             ssn="111-22-3333", relationship="applicant", monthly_income="1500")])
    data = {"program": "housing", "channel": "walk_in", "received_date": TODAY.isoformat(),
            "address": "1 Main St", "city": "Eastside", "zip": "40110", "eviction_date": ""}
    data.update(overrides)
    for i, m in enumerate(members):
        for k, v in m.items():
            data[f"members-{i}-{k}"] = v
    return data


def create(conn, user_id=TERESA, **kw):
    """Create an application directly through the service layer."""
    members = kw.pop("members", [dict(first_name="Ana", last_name="Reyes", dob="1990-05-01",
                                      relationship="applicant", monthly_income="1500")])
    args = dict(user_id=user_id, program="housing", channel="walk_in", received_date=TODAY.isoformat(),
                address="1 Main St", city="Eastside", zip="40110", members=members)
    args.update(kw)
    return db.create_application(conn, **args)
