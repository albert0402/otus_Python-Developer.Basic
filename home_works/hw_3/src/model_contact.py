from typing import Any


class Contact:
    """
    Represents a single contact in the phonebook.
    """

    def __init__(self, id: int, name: str, phone: str, comment: str) -> None:
    
        """
        Initializes a contact with the given details.
        
        Args:
            contact_id (int): Unique identifier for the contact.
            name (str): Name of the contact.
            phone (str): Phone number of the contact.
            comment (str): Additional notes about the contact.
        """
        self.id = id
        self.name = name
        self.phone = phone
        self.comment = comment

    def __str__(self) -> str:
        """
        Returns a string representation of the contact.
        """
        return f"ID: {self.id}, Name: {self.name}, Phone: {self.phone}, Comment: {self.comment}"
    
    def to_dict(self) -> dict[str, Any]:
        """
        Returns a dict representation of the contact.
        """
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "comment": self.comment,
        }