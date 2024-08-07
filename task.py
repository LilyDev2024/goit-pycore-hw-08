import pickle


from classes import AddressBook, Record




def save_data(book, filename="addressbook.pkl"):
   with open(filename, "wb") as f:
       pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
   try:
       with open(filename, "rb") as f:
           return pickle.load(f)
   except FileNotFoundError:
       return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
  


def input_error(func):
   def inner(*args, **kwargs):
       try:
           return func(*args, **kwargs)
       except ValueError:
           return "Give me name and phone please."
       except IndexError:
           return "Enter name please."
   return inner


@input_error
def add_contact(args, book: AddressBook):
   name, phone, *_ = args
   record = book.find(name)
   message = "Contact updated."
   if record is None:
       record = Record(name)
       book.add_record(record)
       message = "Contact added."
   if phone:
       record.add_phone(phone)
   return message


@input_error
def change_contact(args, book: AddressBook):
   name, phone = args
   record = book.find(name)
   if record:
       message = record.edit_phone()
       return message
   else:
       return "There is no such name"  
  
@input_error
def show_phone(args, book: AddressBook):
   name = args[0]
   record = book.find(name)
   telephones = ""
   if record:
       for phone in record.phones:
           telephones += f"{phone}"
           return telephones
   else:
       return "There is no such name"




@input_error
def add_birthday(args, book: AddressBook):
   name, birthday, *_ = args
   record = book.find(name)
   message = "Birthday added."
   if record is None:
       message = "Contact is not found."
       return message
   record.add_birthday(birthday)
   return message




@input_error
def show_birthday(args, book: AddressBook):
   name = args[0]
   record = book.find(name)
   if record:
       return record.birthday
   else:
       return "There is no such name"


@input_error
def birthdays(book: AddressBook):
   birthdays = ""
   if not book:
       return "No contacts"
   for birthday in book.get_upcoming_birthdays():
       birthdays += f"{birthday}"
   return birthdays




def parse_input(user_input):
   cmd, *args = user_input.split()
   cmd = cmd.strip().lower()
   return cmd, args


  
def show_all_contacts(book: AddressBook):
   all_contacts = ""
   for record in book.data.values():
       all_contacts += str(record) + "\n"
   return all_contacts


def main():
   contacts = load_data()
   print("Welcome to the assistant bot!")


   while True:
       user_input = input("Enter a command: ")
       command, args = parse_input(user_input)


       if command in ["close", "exit"]:
           save_data(contacts)
           print("Good bye!")
           break
       elif command == "hello":
           print("How can I help you?")
       elif command == "add":
           print(add_contact(args, contacts))
       elif command == "change":
           print(change_contact(args, contacts))
       elif command == "phone":
           print(show_phone(args, contacts))
       elif command == "all":
           print(show_all_contacts(contacts))
       elif command == "add-birthday":
           print(add_birthday(args, contacts))
       elif command == "show-birthday":
           print(show_birthday(args, contacts))
       elif command == "birthdays":
           print(birthdays(contacts))
       else:
           print("Invalid command.")


if __name__ == "__main__":
   main()











