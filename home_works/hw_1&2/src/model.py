import json
import os

class FileError(Exception):
    """
    Raised when there is an issue with file operations.
    """
    pass

class ContactError(Exception):
    """
    Raised for issues related to contacts.
    """
    pass

class Contact:
    """
    Represents a single contact in the phonebook.
    """

    def __init__(self, id, name, phone, comment):
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

    def __str__(self):
        """
        Returns a string representation of the contact.
        """
        return f"ID: {self.id}, Name: {self.name}, Phone: {self.phone}, Comment: {self.comment}"


class PhoneBook:
    """
    Represents the phone book that manages multiple contacts.
    """

    def __init__(self):
        """
        Initializes an empty phone book.
        """
        self.contacts = []

    def load_from_file(self, file_name):
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

    def save_to_file(self, file_name):
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

    def add_contact(self, name, phone, comment):
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

    def find_contact(self, info):
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

    def update_contact(self, contact_id, name=None, phone=None, comment=None):
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

    def delete_contact(self, contact_id):
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