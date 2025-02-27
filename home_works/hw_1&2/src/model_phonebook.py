import json
import os
from typing import List, Optional
from src.exceptions import FileError, ContactError
from src.model_contact import Contact


class PhoneBook:
    """
    Represents the phone book that manages multiple contacts.
    """

    def __init__(self) -> None:
        """
        Initializes an empty phone book.
        """
        self.contacts: list[Contact] = []

    def load_from_file(self, file_name: str) -> None:
        """
        Loads contacts from a JSON file.

        Args:
            file_name (str): Path to the JSON file.
        
        Raises:
            FileError: If the file does not exist or cannot be read.
        """
        if not os.path.exists(file_name):
            raise FileError(f"File '{file_name}' not found.")
        with open(file_name, 'r') as file:
            try:
                # Load JSON data
                data = json.load(file)  
                # Convert the loaded dictionaries into Contact objects
                self.contacts = [Contact(**contact) for contact in data]
            except json.JSONDecodeError:
                raise FileError(f"File '{file_name}' is not a valid JSON file.")

    def save_to_file(self, file_name: str) -> None:
        """
        Saves all contacts to a JSON file.

        Args:
            file_name (str): Path to save the JSON file.
        
        Raises:
            FileError: If the file cannot be written to.
        """
        try:
            with open(file_name, 'w') as file:
                # Serialize the contacts as dictionaries
                json.dump([contact.__dict__ for contact in self.contacts], file, indent=4)
        except Exception as e:
            raise FileError(f"Failed to save to file '{file_name}': {e}")

    def add_contact(self, name: str, phone: str, comment: str) -> None:
        """
        Adds a new contact to the phone book.

        Args:
            name (str): Name of the contact.
            phone (str): Phone number of the contact.
            comment (str): Additional notes about the contact.
        """
        # Automatically assign a unique ID
        contact_ids = [contact.id for contact in self.contacts]
        max_contact_id = max(contact_ids, default=0) # If list is empty max_contact_id = 0
        contact_id = max_contact_id + 1

        new_contact = Contact(contact_id, name, phone, comment)

        self.contacts.append(new_contact)

    def find_contact(self, info: str) -> List[Contact]:
        """
        Searches for contacts that match the given information.

        Args:
            info (str): Search term (matches ID, name, phone, or comment).
        
        Returns:
            list[Contact]: A list of matching contacts.

        Raises:
            ContactError: If no contacts match the search term.
        """
        results = [contact for contact in self.contacts 
                   if info in (str(contact.id), contact.name, contact.phone, contact.comment)]
        if not results:
            raise ContactError("No contacts found matching the given information.")
        return results

    def update_contact(self,
                        contact_id: int,
                        name: Optional[str] = None,
                        phone: Optional[str] = None,
                        comment: Optional[str] = None) -> None:
        """
        Updates the details of an existing contact.

        Args:
            contact_id (int): ID of the contact to update.
            name (str, optional): New name for the contact.
            phone (str, optional): New phone number for the contact.
            comment (str, optional): New comment for the contact.
        
        Raises:
            ContactError: If the contact with the given ID is not found.
        """
        for contact in self.contacts:
            if contact.id == contact_id:
                # Update only the fields provided
                contact.name = name or contact.name
                contact.phone = phone or contact.phone
                contact.comment = comment or contact.comment
                return
        raise ContactError(f"Contact with ID {contact_id} not found.")

    def delete_contact(self, contact_id: int) -> None:
        """
        Deletes a contact by its ID.

        Args:
            contact_id (int): ID of the contact to delete.
        
        Raises:
            ContactError: If the contact with the given ID is not found.
        """
        for contact in self.contacts:
            if contact.id == contact_id:
                self.contacts.remove(contact)
                return
        raise ContactError(f"Contact with ID {contact_id} not found.")