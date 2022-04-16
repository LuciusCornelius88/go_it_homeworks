import pickle
from collections import UserDict
from copy import deepcopy
from fields import*


class AdressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.iter_index = 0

    # можно сразу передавать несколько записей; если запись с таким именем уже существует, не добавляем ее
    def add_record(self, *records):
        for record in records:
            key = record.name.value
            if key not in self.data:
                self.data[key] = record
            else:
                print(f'Record {key} already exists!')

    def get_record(self, name: Name):
        return self.data.get(name.value)

    # опцию изменения записей реализуем через принцип каррирования; порядок передачи аргументов методу: 1) передаем имя записи;
    # 2) передаем название операции изменения записи; передаем нужные для этой операции данные
    # (новая дата рождения, новая последовательность номеров телефонов, пара "старый номер - новый номер")

    def change_record(self, name: Name, command: str, *args):
        record = self.get_record(name)

        OBJECT_TYPES = {
            'change_birthday': record.change_birthday,
            'add_phone': record.add_phone,
            'change_phone': record.change_phone,
            'delete_phone': record.delete_phone
        }

        def handle_object_types(command, *args):
            func = OBJECT_TYPES.get(command)
            func(*args)

        handle_object_types(command, *args)

    def delete_record(self, *names):
        [self.data.pop(name.value) for name in names]

    # поиск записей на основании совпадений введенной строки с любыми из значений полей объекта записи, case insensitive
    def search_records(self, string: str):
        list_of_records = []

        for record in self.data.values():
            list_of_values = []

            for value in record.__dict__.values():
                if isinstance(value, list):
                    [list_of_values.append(item) for item in value]
                elif value is None:
                    continue
                else:
                    list_of_values.append(value)

            for item in list_of_values:
                if string.lower() in str(item.value).lower():
                    list_of_records.append(record)
                    break

        return list_of_records

    # метод для сериализации
    def save_to_file(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    # метод для десериализации; при восстановлении объекта создаем его глубокую копию
    def restore_from_file(self, filepath):
        with open(filepath, 'rb') as file:
            restored = deepcopy(pickle.load(file))
            return restored

    # определяем итератор, который быдет разбивать вывод словаря на несколько частей
    def __next__(self):
        keys = list(self.data.keys())
        if self.iter_index <= len(self.data)-1:
            self.iter_index += 1
            return self.data[keys[self.iter_index-1]]
        raise StopIteration

    def __iter__(self):
        return self

    def iterator(self, n: int):
        list_of_data = []
        for i in range(n):
            try:
                list_of_data.append(next(self))
            except StopIteration:
                print('Data is over!')
                break

        return list_of_data

    def __deepcopy__(self, memo):
        copy_book = AdressBook()
        memo[id(copy_book)] = copy_book
        copy_book.data = deepcopy(self.data)
        copy_book.iter_index = deepcopy(self.iter_index)
        return copy_book

    def __repr__(self):
        string = f''
        for key, val in self.data.items():
            string += f'Record for name {key}:\n{val}'
        return string

    def __str__(self):
        return self.__repr__()
