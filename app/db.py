"""Persistence (stdlib sqlite3) and the services that combine domain rules with storage."""
import sqlite3
from datetime import date
from pathlib import Path

from app import clock
from app.domain import checklist, deadlines
from app.domain.search import digits, search

SCHEMA = Path(__file__).with_name("schema.sql")
PROGRAMS = {"housing": "Emergency Housing Assistance", "utility": "Utility Relief",
            "child_care": "Child Care Support"}
CHANNELS = {"walk_in": "Walk-in", "phone": "Phone", "mail": "Mail",
            "fax": "Fax (incl. community partners)", "email": "Email"}
RELATIONSHIPS = ["applicant", "spouse/partner", "child", "other"]
APPLIES_TO = {"applicant": "Applicant", "household": "Household (once)",
              "each_adult": "Each member 18+", "each_child": "Each child under 18"}


class ValidationError(ValueError):
    pass


def connect(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA.read_text())
    if not conn.execute("SELECT 1 FROM users").fetchone():
        from app.seed import seed_reference_data
        seed_reference_data(conn)
    conn.commit()


# ---------------------------------------------------------------- users & notifications

def users(conn):
    return [dict(r) for r in conn.execute("SELECT * FROM users ORDER BY id")]


def get_user(conn, user_id):
    r = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(r) if r else None


def notify(conn, user_id, application_id, message):
    conn.execute("INSERT INTO notifications (user_id, application_id, message, created_at) "
                 "VALUES (?, ?, ?, ?)", (user_id, application_id, message, clock.now().isoformat()))


def notifications(conn, user_id):
    return [dict(r) for r in conn.execute(
        "SELECT * FROM notifications WHERE user_id = ? ORDER BY id DESC", (user_id,))]


def unread_count(conn, user_id):
    return conn.execute("SELECT COUNT(*) FROM notifications WHERE user_id = ? AND read = 0",
                        (user_id,)).fetchone()[0]


def mark_notifications_read(conn, user_id):
    conn.execute("UPDATE notifications SET read = 1 WHERE user_id = ?", (user_id,))
    conn.commit()


# ---------------------------------------------------------------- search (DCA-001)

def search_people(conn, criteria: dict) -> list[dict]:
    rows = conn.execute("""
        SELECT p.*, COALESCE(h.address || ', ' || h.city || ' ' || h.zip, '') AS address
        FROM persons p
        LEFT JOIN household_members m ON m.person_id = p.id
        LEFT JOIN households h ON h.id = m.household_id
        GROUP BY p.id""").fetchall()
    found = search([dict(r) for r in rows], criteria)
    for p in found:
        p["applications"] = [dict(r) for r in conn.execute("""
            SELECT a.id, a.program, a.status, a.received_date FROM applications a
            JOIN household_members m ON m.household_id = a.household_id
            WHERE m.person_id = ? ORDER BY a.id""", (p["id"],))]
    return found


def get_person(conn, person_id):
    r = conn.execute("SELECT * FROM persons WHERE id = ?", (person_id,)).fetchone()
    return dict(r) if r else None


# ---------------------------------------------------------------- requirements (DCA-011)

def requirements(conn, program=None, active_only=True):
    sql = "SELECT * FROM document_requirements WHERE 1=1"
    args = []
    if program:
        sql += " AND program = ?"
        args.append(program)
    if active_only:
        sql += " AND active = 1"
    return [dict(r) for r in conn.execute(sql + " ORDER BY program, id", args)]


def add_requirement(conn, program, label, applies_to, condition=None):
    if program not in PROGRAMS or applies_to not in APPLIES_TO or not label.strip():
        raise ValidationError("Program, label and 'applies to' are required.")
    if condition not in (None, "emergency"):
        raise ValidationError("Unknown condition.")
    conn.execute("INSERT INTO document_requirements (program, label, applies_to, condition) "
                 "VALUES (?, ?, ?, ?)", (program, label.strip(), applies_to, condition))
    conn.commit()


def set_requirement_active(conn, requirement_id, active: bool):
    conn.execute("UPDATE document_requirements SET active = ? WHERE id = ?",
                 (int(active), requirement_id))
    conn.commit()


# ---------------------------------------------------------------- applications (DCA-004/033/034/035)

def holidays(conn) -> set[date]:
    return {date.fromisoformat(r[0]) for r in conn.execute("SELECT day FROM holidays")}


def _parse_date(value, field):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field} must be a valid date.")


def create_application(conn, *, user_id, program, channel, received_date, address, city, zip,
                       members, eviction_date=None, emergency=False) -> int:
    """members: list of {first_name, last_name, dob, ssn, relationship, monthly_income, person_id?};
    the first must be the applicant. Returns the new application id."""
    errors = []
    if program not in PROGRAMS:
        errors.append("Choose a program.")
    if channel not in CHANNELS:
        errors.append("Choose how the application arrived.")
    if not (address.strip() and city.strip() and zip.strip()):
        errors.append("Address, city and ZIP are required.")
    received = _parse_date(received_date, "Date received")
    if received > clock.today():
        errors.append("Date received cannot be in the future.")
    eviction = _parse_date(eviction_date, "Eviction date") if eviction_date else None
    if eviction and program != "housing":
        eviction = None
    members = [m for m in members if (m.get("first_name") or "").strip() or m.get("person_id")]
    if not members or members[0].get("relationship") != "applicant":
        errors.append("The first household member must be the applicant.")
    parsed = []
    for i, m in enumerate(members, 1):
        if m.get("person_id"):
            p = get_person(conn, int(m["person_id"]))
            if not p:
                errors.append(f"Member {i}: unknown person.")
                continue
            m = {**m, **{k: p[k] for k in ("first_name", "last_name", "dob", "ssn")}}
        if not (m.get("first_name", "").strip() and m.get("last_name", "").strip() and m.get("dob")):
            errors.append(f"Member {i}: first name, last name and date of birth are required.")
            continue
        ssn = digits(m.get("ssn"))
        if ssn and len(ssn) != 9:
            errors.append(f"Member {i}: SSN must have 9 digits.")
        try:
            income = float(m.get("monthly_income") or 0)
            if income < 0:
                raise ValueError
        except ValueError:
            errors.append(f"Member {i}: monthly income must be a number ≥ 0.")
            income = 0
        parsed.append({**m, "dob": _parse_date(m["dob"], f"Member {i} date of birth"),
                       "ssn": ssn or None, "monthly_income": income,
                       "relationship": m.get("relationship") or "other"})
    if errors:
        raise ValidationError(" ".join(errors))

    due = deadlines.due_date(program, received, eviction, holidays(conn))
    expedited = deadlines.is_expedited(program, received, eviction)
    with conn:
        hh = conn.execute("INSERT INTO households (address, city, zip) VALUES (?, ?, ?)",
                          (address.strip(), city.strip(), zip.strip())).lastrowid
        for m in parsed:
            if m.get("person_id"):
                m["person_id"] = int(m["person_id"])
            else:
                m["person_id"] = conn.execute(
                    "INSERT INTO persons (first_name, last_name, dob, ssn) VALUES (?, ?, ?, ?)",
                    (m["first_name"].strip(), m["last_name"].strip(), m["dob"].isoformat(), m["ssn"])
                ).lastrowid
            conn.execute("INSERT INTO household_members VALUES (?, ?, ?, ?)",
                         (hh, m["person_id"], m["relationship"], m["monthly_income"]))
        app_id = conn.execute("""
            INSERT INTO applications (household_id, program, channel, received_date, eviction_date,
                emergency, expedited, due_date, assigned_to, created_by, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (hh, program, channel, received.isoformat(), eviction and eviction.isoformat(),
             int(bool(emergency)), int(expedited), due.isoformat(), user_id, user_id,
             clock.now().isoformat())).lastrowid
        for line in checklist.build_checklist(requirements(conn, program), parsed, received, emergency):
            conn.execute("INSERT INTO checklist_items (application_id, requirement_id, person_id, label) "
                         "VALUES (?, ?, ?, ?)", (app_id, line["requirement_id"], line["person_id"], line["label"]))
        if expedited:
            applicant = parsed[0]
            msg = (f"EXPEDITED: Housing application #{app_id} ({applicant['first_name']} "
                   f"{applicant['last_name']}) — eviction {eviction.isoformat()}, due {due.isoformat()}")
            notify(conn, user_id, app_id, msg)
            sup = get_user(conn, user_id)["supervisor_id"]
            if sup:
                notify(conn, sup, app_id, msg)
    return app_id


def _with_clock(app: dict, today: date) -> dict:
    due = date.fromisoformat(app["due_date"])
    received = date.fromisoformat(app["received_date"])
    return {**app, "expedited": bool(app["expedited"]),
            "days_remaining": deadlines.days_remaining(due, today),
            "days_elapsed": deadlines.days_elapsed(received, today)}


APP_SELECT = """
    SELECT a.*, p.first_name || ' ' || p.last_name AS applicant_name, u.name AS assigned_name,
        (SELECT COUNT(*) FROM checklist_items c WHERE c.application_id = a.id) AS docs_total,
        (SELECT COUNT(*) FROM checklist_items c JOIN verifications v ON v.checklist_item_id = c.id
         WHERE c.application_id = a.id) AS docs_verified
    FROM applications a
    JOIN household_members m ON m.household_id = a.household_id AND m.relationship = 'applicant'
    JOIN persons p ON p.id = m.person_id
    JOIN users u ON u.id = a.assigned_to"""


def work_queue(conn, user: dict) -> list[dict]:
    """Caseworker: own cases. Supervisor: own team. Program admin: everything."""
    sql, args = APP_SELECT + " WHERE a.status = 'open'", []
    if user["role"] == "caseworker":
        sql += " AND a.assigned_to = ?"
        args = [user["id"]]
    elif user["role"] == "supervisor":
        sql += " AND (a.assigned_to = ? OR u.supervisor_id = ?)"
        args = [user["id"], user["id"]]
    today = clock.today()
    return deadlines.queue_order([_with_clock(dict(r), today) for r in conn.execute(sql, args)])


def get_application(conn, app_id) -> dict | None:
    r = conn.execute(APP_SELECT + " WHERE a.id = ?", (app_id,)).fetchone()
    if not r:
        return None
    app = _with_clock(dict(r), clock.today())
    app["household"] = dict(conn.execute("SELECT * FROM households WHERE id = ?",
                                         (app["household_id"],)).fetchone())
    app["members"] = [dict(x) for x in conn.execute("""
        SELECT p.*, m.relationship, m.monthly_income FROM household_members m
        JOIN persons p ON p.id = m.person_id WHERE m.household_id = ?
        ORDER BY m.relationship != 'applicant', p.dob""", (app["household_id"],))]
    app["checklist"] = checklist_for(conn, app_id)
    return app


# ---------------------------------------------------------------- verification (DCA-012)

def checklist_for(conn, app_id) -> list[dict]:
    return [dict(r) for r in conn.execute("""
        SELECT c.*, v.verified_at, v.document_ref, u.name AS verified_by_name, v.verified_by
        FROM checklist_items c
        LEFT JOIN verifications v ON v.checklist_item_id = c.id
        LEFT JOIN users u ON u.id = v.verified_by
        WHERE c.application_id = ? ORDER BY c.id""", (app_id,))]


class AlreadyVerified(Exception):
    pass


def verify_item(conn, app_id, item_id, user_id, document_ref) -> None:
    if not (document_ref or "").strip():
        raise ValidationError("Describe the document you looked at (e.g. 'Pay stub dated 10/30/2026').")
    item = conn.execute("SELECT id FROM checklist_items WHERE id = ? AND application_id = ?",
                        (item_id, app_id)).fetchone()
    if not item:
        raise LookupError("Checklist item not found.")
    try:
        with conn:
            conn.execute("INSERT INTO verifications (checklist_item_id, verified_by, verified_at, document_ref) "
                         "VALUES (?, ?, ?, ?)", (item_id, user_id, clock.now().isoformat(), document_ref.strip()))
    except sqlite3.IntegrityError:
        raise AlreadyVerified("This item was already verified; verifications cannot be changed.")
