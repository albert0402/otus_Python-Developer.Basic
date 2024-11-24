from src.model import PhoneBook, FileError, ContactError
from src import view
import os

def run_phonebook():
    """
    Orchestrates the phone book application by managing user input, 
    handling the menu, and connecting the model and view.
    """

    FILE_NAME = "contacts.json"

    phonebook = PhoneBook()

    # Get the directory where the current script is located
    directory = os.path.dirname(__file__)

    # Join the directory path with the filename FILE_NAME
    file_name = os.path.join(directory, FILE_NAME)
    
    exit_program = False
    while not exit_program:

        view.display_menu()
        choice = view.get_user_choice()

        try:
            
            # Open file
            if choice == '1':  
                phonebook.load_from_file(file_name)
                view.show_message("File loaded successfully.")
            
            # Save file
            elif choice == '2':  
                phonebook.save_to_file(file_name)
                view.show_message("File saved successfully.")
            
             # Show all contacts
            elif choice == '3': 
                if phonebook.contacts:
                    view.show_contacts(phonebook.contacts)
                else:
                    view.show_message("No contacts to display.")
            
            # Add contact
            elif choice == '4':  
                name, phone, comment = view.get_contact_details()
                phonebook.add_contact(name, phone, comment)
                view.show_message("Contact added successfully.")
            
            # Find contact
            elif choice == '5':  
                info = input("Enter ID, name, phone, or comment to search: ")
                results = phonebook.find_contact(info)
                view.show_contacts(results)
            
            # Change contact
            elif choice == '6':  
                contact_id = int(input("Enter ID of the contact to change: "))
                name, phone, comment = view.get_contact_details()
                phonebook.update_contact(contact_id, name, phone, comment)
                view.show_message("Contact updated successfully.")
            
            # Delete contact
            elif choice == '7':  
                contact_id = int(input("Enter ID of the contact to delete: "))
                phonebook.delete_contact(contact_id)
                view.show_message("Contact deleted successfully.")
            
            # Exit
            elif choice == '8':  
                exit_program = True
                view.show_message("Exiting the program.")
            else:
                view.show_message("Invalid choice. Please try again.")
        
        except (FileError, ContactError) as e:
            view.show_message(str(e))
        
        except ValueError:
            view.show_message("Invalid input. Please enter valid data.")