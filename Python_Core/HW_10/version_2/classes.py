from collections import UserDict, namedtuple


class Field():
    pass


class Name(Field):
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, phone):
        self.phone = phone

    def get_phone(self):
        return self.phone

    def change_phone(self, new_phone):
        self.phone = new_phone


class Record():
    def __init__(self, name):
        self.name = name
        self.phone_list = []

    #реализуем возможность добавлять произвольное количество номеров
    def add_phone(self, *phone):
        list(map(lambda item: self.phone_list.append(item), phone))

    def get_phone_list(self):
        return list(map(lambda phone: phone.get_phone(), self.phone_list))

    #реализуем возможность менять сразу несколько телефонов; для этого нужно передать в метод change_phone последовательность
    #в виде ('старый_телефон', 'новый телефон', 'старый_телефон', 'новый телефон'...);
    #реализуем на основе двух методов:
    #1й метод создает на основе переданной последовательности список именованных кортежей ('старый_телефон', 'новый телефон')
    #2й метод производит изменение в объекте Phone номера телефона для каждого именованного кортежа

    def change_phone(self, *args):
        def create_tuples(*args):
            Phones = namedtuple('Phones', ['old_phone', 'new_phone'])

            tuples = []
            indexes = [i for i in range(len(args)+1)]

            for i in indexes[::2]:
                if indexes.index(i) < len(args):
                    phone = Phones(args[i].get_phone(), args[i+1].get_phone())
                    tuples.append(phone)

            return tuples

        def change(old_phone, new_phone):
            for phone in filter(lambda x: x.get_phone() == old_phone, self.phone_list):
                index = self.phone_list.index(phone)
                self.phone_list[index].change_phone(new_phone)

        phone_tuples = create_tuples(*args)

        for phone_tuple in phone_tuples:
            change(phone_tuple.old_phone, phone_tuple.new_phone)

    #реализуем возможность удалить несколько номеров; метод принимает последовательность номеров, подлежащих удалению
    def delete_phone(self, *phones):
        for phone in phones:
            for item in filter(lambda x: x.get_phone() == phone.get_phone(), self.phone_list):
                self.phone_list.remove(item)


class AdressBook(UserDict):
    def add_record(self, *records):
        for record in records:
            key = record.name.value
            self.data[key] = record

    def get_record(self, name):
        return self.data.get(name)

    def get_all(self):
        return self.data

    def delete_record(self, *names):
        [self.data.pop(key) for key in names]

    # для дальнейшей разработки
    def change_record(self, *args):
        pass

    # для дальнейшей разработки
    def search_in_record(self, *args):
        pass
