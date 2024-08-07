from collections import UserDict
from datetime import datetime, timedelta, date



class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)


class Name(Field):
    pass

class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            birthday = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
            # та перетворіть рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        

class Phone(Field):
    def __init__(self, value: str):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError("Invalid number")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value if self.birthday else ''}"
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                return "Phone was changed"
        return "No such number"
    

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
            
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        deleted_name = self.data.get(name)
        if deleted_name:
            del self.data[name]

    def get_upcoming_birthdays(self):
        current_date = datetime.today().date()
        max = current_date + timedelta(days = 6)
        current_year = current_date.year
        list_of_birthdays = []

        for record in self.data.values():
            birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            next_birthday = date(current_year, birthday.month, birthday.day)

            if next_birthday < current_date:
                next_birthday = date(current_year + 1, birthday.month, birthday.day)
            
            if next_birthday.weekday() == 5:
                next_birthday += timedelta(days=2)

            if next_birthday.weekday() == 6:
                next_birthday += timedelta(days=1)

            if next_birthday <= max and next_birthday >=current_date:
                list_of_birthdays.append({"name": record.name.value, "congratulation_date": next_birthday.strftime("%d.%m.%Y")})

        return list_of_birthdays




if __name__ == "__main__":

# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday('07.08.1997')
    print(john_record.birthday)

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)
    jane_record.add_birthday("08.08.1996")

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    print(book.get_upcoming_birthdays())

    # Видалення запису Jane
    book.delete("Jane")
