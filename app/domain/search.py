"""DCA-001: tolerant person search."""
import re
from difflib import SequenceMatcher

NAME_SIMILARITY = 0.8  # catches Jon/John, Smyth/Smith, Katherine/Catherine


def normalize_name(s: str) -> str:
    """Lowercase letters only: 'Garcia-Lopez', 'Garcia Lopez', 'garcialopez' are all equal."""
    return re.sub(r"[^a-z]", "", (s or "").lower())


def name_parts(s: str) -> list[str]:
    return [normalize_name(p) for p in re.split(r"[-\s]+", s or "") if normalize_name(p)]


def digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def normalize_address(s: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", (s or "").lower()).split())


def name_score(query: str, candidate: str) -> float:
    """1.0 for an exact normalized match; similarity otherwise. Also compares each part of a
    hyphenated/compound name, so 'Garcia' finds 'Garcia-Lopez'."""
    q = normalize_name(query)
    if not q:
        return 1.0
    options = [normalize_name(candidate), *name_parts(candidate)]
    return max(SequenceMatcher(None, q, c).ratio() for c in options if c) if any(options) else 0.0


def ssn_matches(query: str, ssn: str | None) -> bool:
    q = digits(query)
    if not ssn or len(q) not in (4, 9):
        return False
    return ssn.endswith(q) if len(q) == 4 else ssn == q


def match_score(person: dict, criteria: dict) -> float | None:
    """Score a person against search criteria. Every criterion given must match; returns None
    if any fails. Criteria keys: first_name, last_name, dob (ISO), ssn, address."""
    given = {k: (v or "").strip() for k, v in criteria.items() if (v or "").strip()}
    if not given:
        return None
    score = 0.0
    for key in ("first_name", "last_name"):
        if key in given:
            s = name_score(given[key], person[key])
            if s < NAME_SIMILARITY:
                return None
            score += s
    if "dob" in given:
        if given["dob"] != person["dob"]:
            return None
        score += 1
    if "ssn" in given:
        if not ssn_matches(given["ssn"], person.get("ssn")):
            return None
        score += 1
    if "address" in given:
        if normalize_address(given["address"]) not in normalize_address(person.get("address", "")):
            return None
        score += 1
    return score


def search(people: list[dict], criteria: dict) -> list[dict]:
    scored = [(s, p) for p in people if (s := match_score(p, criteria)) is not None]
    return [p for _, p in sorted(scored, key=lambda sp: (-sp[0], sp[1]["last_name"], sp[1]["first_name"]))]
