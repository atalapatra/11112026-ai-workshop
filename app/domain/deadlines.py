"""DCA-033 processing clock, DCA-034 expedited flag, DCA-035 queue ordering."""
from datetime import date, timedelta

STANDARD_DAYS = 30            # calendar days, all programs (00:02:29)
EXPEDITED_WINDOW_DAYS = 7     # eviction within 7 days -> expedited (00:16:36)
EXPEDITED_BUSINESS_DAYS = 3   # 3 business days from receipt (00:16:36)


def is_expedited(program: str, received: date, eviction_date: date | None) -> bool:
    """Housing only. Determined from the eviction date — never from a form checkbox."""
    if program != "housing" or eviction_date is None:
        return False
    return (eviction_date - received).days <= EXPEDITED_WINDOW_DAYS


def add_business_days(start: date, n: int, holidays: set[date]) -> date:
    d = start
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5 and d not in holidays:
            n -= 1
    return d


def due_date(program: str, received: date, eviction_date: date | None, holidays: set[date]) -> date:
    if is_expedited(program, received, eviction_date):
        return add_business_days(received, EXPEDITED_BUSINESS_DAYS, holidays)
    return received + timedelta(days=STANDARD_DAYS)


def days_elapsed(received: date, today: date) -> int:
    return (today - received).days


def days_remaining(due: date, today: date) -> int:
    """Depends only on the due date: nothing (e.g. waiting on documents) pauses the clock."""
    return (due - today).days


def queue_order(apps: list[dict]) -> list[dict]:
    """Expedited first, then soonest due date, then oldest application."""
    return sorted(apps, key=lambda a: (not a["expedited"], a["due_date"], a["id"]))
