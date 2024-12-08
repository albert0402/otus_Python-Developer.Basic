import pytest
from src import view


def test_display_menu(capture_output):
    """Test for displaying the menu."""
    output = capture_output(view.display_menu)
    assert "1. Open file" in output
    assert "8. Exit" in output


@pytest.mark.parametrize(
    "message",
    [
        "Test message",
        "Another message",
        "Hello, world!"
    ],
)
def test_show_message(capture_output, message):
    """Test for displaying a message."""
    output = capture_output(view.show_message, message)
    assert output == message


@pytest.mark.parametrize(
    "contacts, expected_outputs",
    [
        (
            [{"id": 1, "name": "Alice", "phone": "12345", "comment": "Friend"}],
            ["{'id': 1, 'name': 'Alice', 'phone': '12345', 'comment': 'Friend'}"]
        ),
        (
            [
                {"id": 1, "name": "Alice", "phone": "12345", "comment": "Friend"},
                {"id": 2, "name": "Bob", "phone": "67890", "comment": "Colleague"}
            ],
            [
                "{'id': 1, 'name': 'Alice', 'phone': '12345', 'comment': 'Friend'}",
                "{'id': 2, 'name': 'Bob', 'phone': '67890', 'comment': 'Colleague'}"
            ]
        ),
    ],
)
def test_show_contacts(capture_output, contacts, expected_outputs):
    """Test for displaying the list of contacts."""
    output = capture_output(view.show_contacts, contacts)
    for expected in expected_outputs:
        assert expected in output
