"""Single source of 'today' and 'now'. Override in tests with set_today(); in demos with DCA_TODAY."""
import os
from datetime import date, datetime

_today_override: date | None = None


def today() -> date:
    if _today_override:
        return _today_override
    env = os.environ.get("DCA_TODAY")
    return date.fromisoformat(env) if env else date.today()


def now() -> datetime:
    return datetime.now().replace(microsecond=0)


def set_today(d: date | None) -> None:
    global _today_override
    _today_override = d
