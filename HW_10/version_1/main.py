from classes import*

# тестирование модуля с определениями классов


def main():
    name_1 = Name('name_1')
    name_2 = Name('name_2')
    record_1 = Record(name_1.value)
    record_2 = Record(name_2.value)

    record_1.add_phone('88858585858', '959595959', '75747474747')
    print(record_1.get_phone_list())

    record_1.change_phone('959595959', '999999999999', '88858585858', '888888')
    print(record_1.get_phone_list())

    record_1.delete_phone('888888')
    print(record_1.get_phone_list())

    book = AdressBook()
    book.add_record(record_1, record_2)
    print(book.get_all())
    print(book.get_record(name_2.value))

    book.delete_record(name_2.value)
    print(book.get_all())


if __name__ == '__main__':
    main()
