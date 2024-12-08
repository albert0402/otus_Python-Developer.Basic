import pytest

from src.controller import run_phonebook
from src.model_phonebook import PhoneBook
from src import view
from src.exceptions import FileError, ContactError


def test_run_phonebook_open_and_exit(monkeypatch):
    """
    Simulates user input for opening a file and exiting the application.
    """
    inputs = iter(["1", "8"])  # Simulates selecting 'Open file' and then 'Exit'
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    phonebook = PhoneBook()
    monkeypatch.setattr("src.controller.PhoneBook", lambda: phonebook)

    assert run_phonebook() is None


def test_run_phonebook_add_and_display_contacts(monkeypatch, capsys):
    """
    Simulates user input for adding a contact and displaying contacts.
    """
    inputs = iter(["4", "Alice", "12345", "Friend", "3", "8"])  # Add contact, display, exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    phonebook = PhoneBook()
    monkeypatch.setattr("src.controller.PhoneBook", lambda: phonebook)

    run_phonebook()
    captured = capsys.readouterr()

    assert "Contact added successfully." in captured.out
    assert "ID: 1, Name: Alice, Phone: 12345, Comment: Friend" in captured.out


def test_run_phonebook_find_contact(monkeypatch, capsys):
    """
    Simulates user input for finding a contact.
    """
    inputs = iter(["5", "Alice", "8"])  # Find contact, exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    phonebook = PhoneBook()
    phonebook.add_contact("Alice", "12345", "Friend")
    monkeypatch.setattr("src.controller.PhoneBook", lambda: phonebook)

    run_phonebook()
    captured = capsys.readouterr()

    assert "ID: 1, Name: Alice, Phone: 12345, Comment: Friend" in captured.out


def test_run_phonebook_update_contact(monkeypatch, capsys):
    """
    Simulates user input for updating a contact.
    """
    inputs = iter(["6", "1", "Alice Updated", "54321", "Best Friend", "3", "8"])  # Update, display, exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    phonebook = PhoneBook()
    phonebook.add_contact("Alice", "12345", "Friend")
    monkeypatch.setattr("src.controller.PhoneBook", lambda: phonebook)

    run_phonebook()
    captured = capsys.readouterr()

    assert "Contact updated successfully." in captured.out
    assert "ID: 1, Name: Alice Updated, Phone: 54321, Comment: Best Friend" in captured.out


def test_run_phonebook_delete_contact(monkeypatch, capsys):
    """
    Simulates user input for deleting a contact.
    """
    inputs = iter(["7", "1", "3", "8"])  # Delete, display, exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    phonebook = PhoneBook()
    phonebook.add_contact("Alice", "12345", "Friend")
    monkeypatch.setattr("src.controller.PhoneBook", lambda: phonebook)

    run_phonebook()
    captured = capsys.readouterr()

    assert "Contact deleted successfully." in captured.out
    assert "No contacts to display." in captured.out


def test_run_phonebook_invalid_choice(monkeypatch, capsys):
    """
    Simulates user input of an invalid menu choice.
    """
    inputs = iter(["9", "8"])  # Invalid option, then exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    phonebook = PhoneBook()
    monkeypatch.setattr("src.controller.PhoneBook", lambda: phonebook)

    run_phonebook()
    captured = capsys.readouterr()

    assert "Invalid choice. Please try again." in captured.out


def test_run_phonebook_load_invalid_file(monkeypatch, capsys):
    """
    Simulates loading a non-existent or invalid file.
    """
    inputs = iter(["1", "8"])  # Load file, then exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    def mock_load_from_file(file_name):
        raise FileError("File not found or invalid format.")

    phonebook = PhoneBook()
    monkeypatch.setattr(phonebook, "load_from_file", mock_load_from_file)
    monkeypatch.setattr("src.controller.PhoneBook", lambda: phonebook)

    run_phonebook()
    captured = capsys.readouterr()

    assert "File not found or invalid format." in captured.out


def test_run_phonebook_invalid_input(monkeypatch, capsys):
    """
    Simulates invalid input when numeric input is required.
    """
    inputs = iter(["6", "invalid_id", "8"])  # Invalid contact ID, then exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    phonebook = PhoneBook()
    phonebook.add_contact("Alice", "12345", "Friend")
    monkeypatch.setattr("src.controller.PhoneBook", lambda: phonebook)

    run_phonebook()
    captured = capsys.readouterr()

    assert "Invalid input. Please enter valid data." in captured.out