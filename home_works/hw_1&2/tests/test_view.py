from io import StringIO
import sys
from src import view

# Helper function to capture output
def capture_output(func, *args, **kwargs):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        func(*args, **kwargs)
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdout = old_stdout

def test_display_menu():
    output = capture_output(view.display_menu)
    assert "1. Open file" in output
    assert "8. Exit" in output

def test_show_message():
    output = capture_output(view.show_message, "Test message")
    assert output == "Test message"

def test_show_contacts():
    contacts = [
        {"id": 1, "name": "Alice", "phone": "12345", "comment": "Friend"},
        # {"id": 2, "name": "Bob", "phone": "67890", "comment": "Colleague"}
    ]
    output = capture_output(view.show_contacts, contacts)
    assert "{'id': 1, 'name': 'Alice', 'phone': '12345', 'comment': 'Friend'}" in output
    


