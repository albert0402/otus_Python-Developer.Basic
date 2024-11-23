def display_menu():
    """
    Displays the main menu with available options.
    """
    print("\nPhone Book Menu\n"
        "Choose an option (1-8):\n"
        "1. Open file: Load contacts from a JSON file.\n"
        "2. Save file: Save the current contacts to a JSON file.\n"
        "3. Show all contacts: Display all saved contacts.\n"
        "4. Add contact: Add a new contact with name, phone, and comment.\n"
        "5. Find contact: Search for a contact by ID, name, phone, or comment.\n"
        "6. Change contact: Update the details of an existing contact by ID.\n"
        "7. Delete contact: Remove a contact from the phone book by ID.\n"
        "8. Exit: Exit the program.\n")


def get_user_choice():
    """
    Prompts the user to choose a menu option.

    Returns:
        str: The user's choice as a string.
    """
    return input("Choose an option (1-8): ")


def get_contact_details():
    """
    Prompts the user to input contact details.

    Returns:
        tuple: A tuple containing name, phone, and comment as strings.
    """
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    comment = input("Enter comment: ")
    return name, phone, comment


def show_contacts(contacts):
    """
    Displays a list of contacts.

    Args:
        contacts (list[Contact]): A list of Contact objects to display.
    """
    for contact in contacts:
        print(contact)


def show_message(message):
    """
    Displays a message to the user.

    Args:
        message (str): The message to display.
    """
    print(message)