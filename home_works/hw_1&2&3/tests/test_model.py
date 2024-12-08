import pytest
import json
import pytest
from src.model_phonebook import PhoneBook
from src.exceptions import FileError, ContactError


@pytest.mark.parametrize(
    "name, phone, comment",
    [
        ("Alice", "12345", "Friend"),
        ("Bob", "67890", "Colleague"),
        ("Charlie", "54321", "Neighbor"),
    ],
)
def test_add_contact(empty_phonebook, name, phone, comment):
    empty_phonebook.add_contact(name, phone, comment)
    assert len(empty_phonebook.contacts) == 1
    assert empty_phonebook.contacts[0].name == name
    assert empty_phonebook.contacts[0].phone == phone
    assert empty_phonebook.contacts[0].comment == comment


@pytest.mark.parametrize(
    "search_term, expected_count",
    [
        ("Alice", 1),
        ("67890", 1),
        ("Nonexistent", 0),
    ],
)
def test_find_contact(sample_phonebook, search_term, expected_count):
    if expected_count > 0:
        results = sample_phonebook.find_contact(search_term)
        assert len(results) == expected_count
    else:
        with pytest.raises(ContactError):
            sample_phonebook.find_contact(search_term)


def test_update_contact(sample_phonebook):
    sample_phonebook.update_contact(1, name="Alicia", phone="54321")
    assert sample_phonebook.contacts[0].name == "Alicia"
    assert sample_phonebook.contacts[0].phone == "54321"


def test_delete_contact(sample_phonebook):
    sample_phonebook.delete_contact(1)
    assert len(sample_phonebook.contacts) == 1
    assert sample_phonebook.contacts[0].name == "Bob"


def test_load_from_file(tmp_json_file):
    phonebook = PhoneBook()
    phonebook.load_from_file(tmp_json_file)
    assert len(phonebook.contacts) == 1
    assert phonebook.contacts[0].name == "Alice"


def test_load_from_invalid_json(invalid_json_file):
    phonebook = PhoneBook()
    with pytest.raises(FileError):
        phonebook.load_from_file(invalid_json_file)


def test_save_to_file(sample_phonebook, tmp_path):
    file_path = tmp_path / "contacts.json"
    sample_phonebook.save_to_file(str(file_path))
    saved_data = json.loads(file_path.read_text())
    assert len(saved_data) == 2
    assert saved_data[0]["name"] == "Alice"
    assert saved_data[1]["name"] == "Bob"