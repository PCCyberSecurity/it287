import os
import json
import colorama
colorama.init()


class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"{self.name},{self.phone},{self.email}"
    
    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }

def save_contacts(contacts):
    json_contacts = []
    for contact in contacts:
        json_contacts.append(contact.to_dict())
    with open("contacts.json", "w") as f:
        json.dump(json_contacts, f, indent=4)

    with open("contacts.csv", "w") as f:
        for contact in contacts:
            f.write(str(contact) + "\n")
    return True

def load_contacts():
    contacts = []
    # if os.path.exists("contacts.csv"):
    #     with open("contacts.csv", "r") as f:
    #         for line in f:
    #             parts = line.strip().split(",")
    #             if len(parts) == 3:
    #                 name, phone, email = parts
    #                 contacts.append(Contact(name, phone, email))

    if os.path.exists("contacts.json"):
        with open("contacts.json", "r") as f:
            json_contacts = json.load(f)
            for jc in json_contacts:
                contacts.append(Contact(jc["name"], jc["phone"], jc["email"]))
    return contacts

def main():
    contacts = load_contacts()

    while True:
        print(colorama.Fore.GREEN + "Welcome to the contact list application." + colorama.Style.RESET_ALL)
        print("[A]  Add a new contact")
        print("[V]  View all contacts")
        print("[D]  Delete a contact")
        print("[S]  Save Contacts")
        print("[Q]  Quit")
        choice = input("Choose an option: ").strip().upper()
        if choice == "Q":
            save_contacts(contacts)
            print(colorama.Fore.RED + "Exiting the contact list application." + colorama.Style.RESET_ALL)
            break
        elif choice == "A":
            name = input("Enter name: ").strip()
            phone = input("Enter phone: ").strip()
            email = input("Enter email: ").strip()
            contact = Contact(name, phone, email)
            contacts.append(contact)
            print(colorama.Fore.BLUE + "Contact added: " + str(contact) + colorama.Style.RESET_ALL)
            save_contacts(contacts)
            continue
        elif choice == "V":
            if not contacts:
                print(colorama.Fore.YELLOW + "No contacts to display." + colorama.Style.RESET_ALL)
            else:
                for contact in contacts:
                    print(contact)
            continue
        elif choice == "S":
            save_contacts(contacts)

if __name__ == "__main__":
    main()