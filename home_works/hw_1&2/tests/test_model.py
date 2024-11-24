import pytest
import json
from src.model import PhoneBook, Contact, FileError, ContactError

# Helper function to create a sample phonebook with contacts
def create_sample_phonebook():
    phonebook = PhoneBook()
    phonebook.add_contact("Alice", "12345", "Friend")
    phonebook.add_contact("Bob", "67890", "Colleague")
    return phonebook

# Tests for Contact class
def test_contact_initialization():
    contact = Contact(1, "Alice", "12345", "Friend")
    assert contact.id == 1
    assert contact.name == "Alice"
    assert contact.phone == "12345"
    assert contact.comment == "Friend"
    assert str(contact) == "ID: 1, Name: Alice, Phone: 12345, Comment: Friend"

# Tests for PhoneBook class
def test_phonebook_initialization():
    phonebook = PhoneBook()
    assert phonebook.contacts == []

def test_add_contact():
    phonebook = PhoneBook()
    phonebook.add_contact("Alice", "12345", "Friend")
    assert len(phonebook.contacts) == 1
    assert phonebook.contacts[0].name == "Alice"

def test_add_contact_with_existing_contacts():
    phonebook = create_sample_phonebook()
    phonebook.add_contact("Charlie", "54321", "Neighbor")
    assert len(phonebook.contacts) == 3
    assert phonebook.contacts[-1].name == "Charlie"

def test_find_contact_by_name():
    phonebook = create_sample_phonebook()
    results = phonebook.find_contact("Alice")
    assert len(results) == 1
    assert results[0].name == "Alice"

def test_find_contact_by_phone():
    phonebook = create_sample_phonebook()
    results = phonebook.find_contact("67890")
    assert len(results) == 1
    assert results[0].phone == "67890"

def test_find_contact_no_match():
    phonebook = create_sample_phonebook()
    with pytest.raises(ContactError):
        phonebook.find_contact("Nonexistent")

def test_update_contact():
    phonebook = create_sample_phonebook()
    phonebook.update_contact(1, name="Alicia", phone="54321")
    assert phonebook.contacts[0].name == "Alicia"
    assert phonebook.contacts[0].phone == "54321"

def test_update_contact_invalid_id():
    phonebook = create_sample_phonebook()
    with pytest.raises(ContactError):
        phonebook.update_contact(99, name="NewName")

def test_delete_contact():
    phonebook = create_sample_phonebook()
    phonebook.delete_contact(1)
    assert len(phonebook.contacts) == 1
    assert phonebook.contacts[0].name == "Bob"

def test_delete_contact_invalid_id():
    phonebook = create_sample_phonebook()
    with pytest.raises(ContactError):
        phonebook.delete_contact(99)

def test_load_from_file(tmp_path):
    file_path = tmp_path / "contacts.json"
    sample_data = [{"id": 1, "name": "Alice", "phone": "12345", "comment": "Friend"}]
    file_path.write_text(json.dumps(sample_data))

    phonebook = PhoneBook()
    phonebook.load_from_file(str(file_path))

    assert len(phonebook.contacts) == 1
    assert phonebook.contacts[0].name == "Alice"

def test_load_from_file_nonexistent():
    phonebook = PhoneBook()
    with pytest.raises(FileError):
        phonebook.load_from_file("nonexistent.json")

def test_load_from_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text("{invalid_json")

    phonebook = PhoneBook()
    with pytest.raises(FileError):
        phonebook.load_from_file(str(file_path))

def test_save_to_file(tmp_path):
    phonebook = create_sample_phonebook()
    file_path = tmp_path / "contacts.json"

    phonebook.save_to_file(str(file_path))
    saved_data = json.loads(file_path.read_text())

    assert len(saved_data) == 2
    assert saved_data[0]["name"] == "Alice"
    assert saved_data[1]["name"] == "Bob"