from pathlib import Path
from adress_book import AdressBook
from record import Record
from fields import*


def main():
    name_1 = Name('Vavan')
    name_2 = Name('Benya')
    name_3 = Name('Doda')
    name_4 = Name('Dimon')
    name_5 = Name('Sasha')
    name_6 = Name('Senya')
    name_7 = Name('Ahmed')

    record_1 = Record(name_1)
    record_1.birthday = Birthday('10/05/1994')

    phone_1 = Phone('+380935034975')
    phone_1.value = '945548485'

    record_1.add_phone(phone_1)

    phone_2 = Phone('+380932034975')
    phone_3 = Phone('+380935034922')
    record_1.add_phone(phone_2, phone_3)

    record_1.get_phone_list()

    record_1.delete_phone(phone_3)
    record_1.get_phone_list()

    record_1.days_to_birthday()

    record_2 = Record(name_2)
    record_3 = Record(name_3)
    record_4 = Record(name_4)
    record_5 = Record(name_5)
    record_6 = Record(name_6)
    record_7 = Record(name_7)

    book = AdressBook()
    book.add_record(record_1, record_2, record_3, record_4,
                    record_5, record_4, record_6, record_7)

    print(book.get_record(name_2))

    book.delete_record(name_2)

    birthday_2 = Birthday('24/10/2015')

    book.change_record(name_1, 'change_birthday', birthday_2)
    book.change_record(name_1, 'change_phone', phone_1, phone_3)

    path = Path(r'C:\Users\user\Desktop\Python\GO_IT\Files\data.bin')
    book.save_to_file(path)

    book_1 = book.restore_from_file(path)

    print(book.iterator(5))
    print(book.iterator(5))

    book.change_record(name_1, 'add_phone', Phone('+380555034977'))
    book_1.change_record(name_1, 'add_phone', Phone('+380555031177'))

    print(book_1.iterator(5))

    print(book_1 is book)

    print(book.search_records('2015'))


if __name__ == '__main__':
    main()
