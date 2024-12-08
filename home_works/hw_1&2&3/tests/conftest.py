import pytest
from src.model_phonebook import PhoneBook
from io import StringIO
import sys
import json


@pytest.fixture
def empty_phonebook() -> PhoneBook:
    """Fixture for creating an empty phonebook."""
    return PhoneBook()


@pytest.fixture
def sample_phonebook() -> PhoneBook:
    """Fixture for creating a phonebook with sample data."""
    phonebook = PhoneBook()
    phonebook.add_contact("Alice", "12345", "Friend")
    phonebook.add_contact("Bob", "67890", "Colleague")
    return phonebook


@pytest.fixture
def tmp_json_file(tmp_path) -> str:
    """Fixture for creating a temporary JSON file."""
    file_path = tmp_path / "contacts.json"
    sample_data = [{"id": 1, "name": "Alice", "phone": "12345", "comment": "Friend"}]
    file_path.write_text(json.dumps(sample_data))
    return str(file_path)


@pytest.fixture
def invalid_json_file(tmp_path) -> str:
    """Fixture for creating a temporary file with invalid JSON content."""
    file_path = tmp_path / "invalid.json"
    file_path.write_text("{invalid_json")
    return str(file_path)


@pytest.fixture
def capture_output():
    """Helper fixture for capturing function output."""
    def _capture_output(func, *args, **kwargs):
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            func(*args, **kwargs)
            return sys.stdout.getvalue().strip()
        finally:
            sys.stdout = old_stdout
    return _capture_output
