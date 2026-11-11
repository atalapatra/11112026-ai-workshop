-- DCA case management: slice 1 (intake to deadline)

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    role          TEXT NOT NULL CHECK (role IN ('caseworker', 'supervisor', 'program_admin')),
    supervisor_id INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS holidays (
    day  TEXT PRIMARY KEY,           -- ISO date
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS persons (
    id         INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    dob        TEXT NOT NULL,        -- ISO date
    ssn        TEXT                  -- 9 digits, no formatting; optional
);

CREATE TABLE IF NOT EXISTS households (
    id      INTEGER PRIMARY KEY,
    address TEXT NOT NULL,
    city    TEXT NOT NULL,
    zip     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS household_members (
    household_id   INTEGER NOT NULL REFERENCES households(id),
    person_id      INTEGER NOT NULL REFERENCES persons(id),
    relationship   TEXT NOT NULL,     -- applicant, spouse/partner, child, other
    monthly_income REAL NOT NULL DEFAULT 0,
    PRIMARY KEY (household_id, person_id)
);

CREATE TABLE IF NOT EXISTS applications (
    id            INTEGER PRIMARY KEY,
    household_id  INTEGER NOT NULL REFERENCES households(id),
    program       TEXT NOT NULL CHECK (program IN ('housing', 'utility', 'child_care')),
    channel       TEXT NOT NULL CHECK (channel IN ('walk_in', 'phone', 'mail', 'fax', 'email')),
    received_date TEXT NOT NULL,
    eviction_date TEXT,
    emergency     INTEGER NOT NULL DEFAULT 0,
    expedited     INTEGER NOT NULL DEFAULT 0,
    due_date      TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'open',
    assigned_to   INTEGER NOT NULL REFERENCES users(id),
    created_by    INTEGER NOT NULL REFERENCES users(id),
    created_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS document_requirements (
    id         INTEGER PRIMARY KEY,
    program    TEXT NOT NULL,
    label      TEXT NOT NULL,
    applies_to TEXT NOT NULL CHECK (applies_to IN ('applicant', 'household', 'each_adult', 'each_child')),
    condition  TEXT CHECK (condition IN ('emergency')),
    active     INTEGER NOT NULL DEFAULT 1
);

-- Snapshot of requirements at intake: later admin changes don't rewrite existing applications.
CREATE TABLE IF NOT EXISTS checklist_items (
    id             INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL REFERENCES applications(id),
    requirement_id INTEGER NOT NULL REFERENCES document_requirements(id),
    person_id      INTEGER REFERENCES persons(id),
    label          TEXT NOT NULL
);

-- Append-only verification record (DCA-012). Triggers below make it immutable.
CREATE TABLE IF NOT EXISTS verifications (
    id                INTEGER PRIMARY KEY,
    checklist_item_id INTEGER NOT NULL UNIQUE REFERENCES checklist_items(id),
    verified_by       INTEGER NOT NULL REFERENCES users(id),
    verified_at       TEXT NOT NULL,
    document_ref      TEXT NOT NULL
);

CREATE TRIGGER IF NOT EXISTS verifications_no_update
BEFORE UPDATE ON verifications
BEGIN SELECT RAISE(ABORT, 'verifications are immutable'); END;

CREATE TRIGGER IF NOT EXISTS verifications_no_delete
BEFORE DELETE ON verifications
BEGIN SELECT RAISE(ABORT, 'verifications are immutable'); END;

CREATE TABLE IF NOT EXISTS notifications (
    id             INTEGER PRIMARY KEY,
    user_id        INTEGER NOT NULL REFERENCES users(id),
    application_id INTEGER REFERENCES applications(id),
    message        TEXT NOT NULL,
    created_at     TEXT NOT NULL,
    read           INTEGER NOT NULL DEFAULT 0
);
