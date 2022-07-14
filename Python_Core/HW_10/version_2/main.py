from classes import*

# тестирование модуля с определениями классов


def main():
    name_1 = Name('name_1')
    name_2 = Name('name_2')
    record_1 = Record(name_1)
    record_2 = Record(name_2)

    phone_1 = Phone('88858585858')
    phone_2 = Phone('959595959')
    phone_3 = Phone('75747474747')

    record_1.add_phone(phone_1, phone_2, phone_3)
    print(record_1.get_phone_list())

    new_phone_1 = Phone('888888')
    new_phone_2 = Phone('999999999999')

    record_1.change_phone(phone_1, new_phone_1, phone_2, new_phone_2)
    print(record_1.get_phone_list())

    record_1.delete_phone(new_phone_1, phone_3)
    print(record_1.get_phone_list())

    book = AdressBook()
    book.add_record(record_1, record_2)
    print(book.get_all())
    print(book.get_record(name_2.value))

    book.delete_record(name_2.value)
    print(book.get_all())


if __name__ == '__main__':
    main()
