"""DCA-001: Find existing people with tolerant search."""
import pytest

from app.domain.search import search
from tests.conftest import create

PEOPLE = [
    {"id": 1, "first_name": "Maria", "last_name": "Garcia-Lopez", "dob": "1986-04-02", "ssn": "123456789",
     "address": "18 Birch Lane, Eastside 40112"},
    {"id": 2, "first_name": "John", "last_name": "Smith", "dob": "1971-01-30", "ssn": "987654321",
     "address": "402 Market St Apt 3, Eastside 40110"},
    {"id": 3, "first_name": "John", "last_name": "Smith", "dob": "1999-06-11", "ssn": None,
     "address": "402 Market St Apt 3, Eastside 40110"},
    {"id": 4, "first_name": "Katherine", "last_name": "O'Neal", "dob": "1980-07-19", "ssn": None,
     "address": "9 Orchard Rd, Riverton 40221"},
]


def ids(results):
    return [p["id"] for p in results]


@pytest.mark.story("DCA-001", 1)
@pytest.mark.parametrize("criteria, expected", [
    ({"last_name": "Smith"}, [2, 3]),
    ({"dob": "1999-06-11"}, [3]),
    ({"ssn": "987654321"}, [2]),
    ({"ssn": "6789"}, [1]),
    ({"address": "orchard rd"}, [4]),
    ({"first_name": "John", "last_name": "Smith", "dob": "1971-01-30"}, [2]),  # father vs son
])
def test_search_by_each_field(criteria, expected):
    assert sorted(ids(search(PEOPLE, criteria))) == expected


@pytest.mark.story("DCA-001", 2)
@pytest.mark.parametrize("last_name", ["Garcia Lopez", "GarciaLopez", "garcia-lopez", "Garcia", "Lopez", "Garsia-Lopez"])
def test_hyphen_spacing_and_spelling_variants_find_hyphenated_name(last_name):
    assert ids(search(PEOPLE, {"last_name": last_name})) == [1]


@pytest.mark.story("DCA-001", 2)
@pytest.mark.parametrize("first, last, expected", [
    ("Jon", "Smyth", [2, 3]), ("Catherine", "ONeal", [4]), ("Katherine", "O Neal", [4]),
])
def test_spelling_variants(first, last, expected):
    assert sorted(ids(search(PEOPLE, {"first_name": first, "last_name": last}))) == expected


@pytest.mark.story("DCA-001", 2)
def test_dissimilar_names_do_not_match():
    assert search(PEOPLE, {"last_name": "Johnson"}) == []


@pytest.mark.story("DCA-001", 3)
@pytest.mark.parametrize("ssn", ["123-45-6789", "123456789", "123 45 6789", " 6789 "])
def test_ssn_matches_regardless_of_format(ssn):
    assert ids(search(PEOPLE, {"ssn": ssn})) == [1]


@pytest.mark.story("DCA-001", 3)
def test_partial_ssn_other_than_last_four_does_not_match():
    assert search(PEOPLE, {"ssn": "12345"}) == []


@pytest.mark.story("DCA-001", 4)
def test_name_and_dob_alone_finds_person_without_ssn():
    assert ids(search(PEOPLE, {"first_name": "Katherine", "last_name": "O'Neal", "dob": "1980-07-19"})) == [4]


@pytest.mark.story("DCA-001", 4)
def test_search_page_end_to_end(client, conn):
    create(conn, members=[dict(first_name="Maria", last_name="Garcia-Lopez", dob="1986-04-02",
                               ssn="123-45-6789", relationship="applicant")])
    r = client.post("/search", data={"last_name": "Garcia Lopez", "dob": "1986-04-02", "ssn": "6789"})
    assert r.status_code == 200
    assert "Maria Garcia-Lopez" in r.text
    assert "1 match" in r.text
    assert "123-45-6789" not in r.text and "6789" in r.text  # SSN masked in results


@pytest.mark.story("DCA-001", 3)
def test_search_form_posts_so_ssn_never_lands_in_url(client):
    page = client.get("/search").text
    assert '<form method="post" action="/search"' in page
