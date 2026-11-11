"""Reference data (always loaded) and demo data (`python -m app.seed --demo`). All people are fictional."""
import argparse
import os
from datetime import timedelta

from app import clock, db

USERS = [  # id, name, role, supervisor_id
    (1, "Marcus Oyelaran", "supervisor", None),
    (2, "Teresa Alvarez", "caseworker", 1),
    (3, "Andre Wilson", "caseworker", 1),
    (4, "Pat Kim", "program_admin", None),
]

REQUIREMENTS = [  # program, label, applies_to, condition  (transcript 00:07:33)
    ("housing", "Photo ID", "applicant", None),
    ("housing", "Lease", "household", None),
    ("housing", "Eviction notice or past-due notice from landlord", "household", None),
    ("housing", "Proof of income", "each_adult", None),
    ("utility", "Photo ID", "applicant", None),
    ("utility", "Proof of income", "household", None),
    ("utility", "Utility bill", "household", None),
    ("utility", "Shutoff notice", "household", "emergency"),
    ("child_care", "Proof of income", "household", None),
    ("child_care", "Proof of work or school", "applicant", None),
    ("child_care", "Birth certificate or equivalent", "each_child", None),
]

HOLIDAYS = [  # US federal holidays (observed) — stand-in for the state calendar
    ("2026-01-01", "New Year's Day"), ("2026-01-19", "MLK Day"), ("2026-02-16", "Presidents' Day"),
    ("2026-05-25", "Memorial Day"), ("2026-06-19", "Juneteenth"), ("2026-07-03", "Independence Day (observed)"),
    ("2026-09-07", "Labor Day"), ("2026-10-12", "Columbus Day"), ("2026-11-11", "Veterans Day"),
    ("2026-11-26", "Thanksgiving"), ("2026-12-25", "Christmas Day"),
    ("2027-01-01", "New Year's Day"), ("2027-01-18", "MLK Day"), ("2027-02-15", "Presidents' Day"),
    ("2027-05-31", "Memorial Day"), ("2027-06-18", "Juneteenth (observed)"),
    ("2027-07-05", "Independence Day (observed)"), ("2027-09-06", "Labor Day"),
    ("2027-10-11", "Columbus Day"), ("2027-11-11", "Veterans Day"), ("2027-11-25", "Thanksgiving"),
    ("2027-12-24", "Christmas Day (observed)"), ("2027-12-31", "New Year's Day (observed)"),
]


def seed_reference_data(conn):
    conn.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", USERS)
    conn.executemany("INSERT INTO document_requirements (program, label, applies_to, condition) "
                     "VALUES (?, ?, ?, ?)", REQUIREMENTS)
    conn.executemany("INSERT INTO holidays VALUES (?, ?)", HOLIDAYS)


def seed_demo_data(conn):
    """A handful of applications at different points on the clock, relative to today."""
    t = clock.today()
    d = lambda n: (t - timedelta(days=n)).isoformat()
    demo = [
        dict(user_id=2, program="utility", channel="phone", received_date=d(24), emergency=True,
             address="18 Birch Lane", city="Eastside", zip="40112",
             members=[dict(first_name="Maria", last_name="Garcia-Lopez", dob="1986-04-02", ssn="123-45-6789",
                           relationship="applicant", monthly_income="1850"),
                      dict(first_name="Luis", last_name="Garcia", dob="2015-09-14", relationship="child")]),
        dict(user_id=2, program="housing", channel="walk_in", received_date=d(1),
             eviction_date=(t + timedelta(days=5)).isoformat(),
             address="402 Market St Apt 3", city="Eastside", zip="40110",
             members=[dict(first_name="John", last_name="Smith", dob="1971-01-30", ssn="987654321",
                           relationship="applicant", monthly_income="2100"),
                      dict(first_name="John", last_name="Smith", dob="1999-06-11", relationship="other",
                           monthly_income="900")]),
        dict(user_id=3, program="child_care", channel="fax", received_date=d(12),
             address="77 Elm Court", city="Riverton", zip="40220",
             members=[dict(first_name="Lan", last_name="Nguyen", dob="1992-12-01", ssn="555-12-3456",
                           relationship="applicant", monthly_income="2400"),
                      dict(first_name="Bao", last_name="Nguyen", dob="2021-03-08", relationship="child")]),
        dict(user_id=3, program="housing", channel="mail", received_date=d(27),
             eviction_date=(t + timedelta(days=40)).isoformat(),
             address="9 Orchard Rd", city="Riverton", zip="40221",
             members=[dict(first_name="Keisha", last_name="O'Neal", dob="1980-07-19",
                           relationship="applicant", monthly_income="1600")]),
    ]
    for kwargs in demo:
        db.create_application(conn, **kwargs)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Create a fresh database with reference + demo data.")
    ap.add_argument("--db", default=os.environ.get("DCA_DB", "dca.db"))
    a = ap.parse_args()
    if os.path.exists(a.db):
        os.remove(a.db)
    conn = db.connect(a.db)
    db.init_db(conn)
    seed_demo_data(conn)
    conn.commit()
    print(f"Seeded {a.db}")
