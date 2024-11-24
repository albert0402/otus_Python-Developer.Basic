import pytest

from src.controller import run_phonebook
from src.model import PhoneBook, FileError, ContactError
from src import view

def test_run_phonebook(monkeypatch):
    # Simulate user input for menu
    inputs = iter(["1", "8"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Simulate file load
    phonebook = PhoneBook()
    monkeypatch.setattr("src.controller.PhoneBook", lambda: phonebook)
    
    # Ensure the program runs without errors
    assert run_phonebook() is None  
