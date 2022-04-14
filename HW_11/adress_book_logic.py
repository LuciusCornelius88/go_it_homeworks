import re
from datetime import datetime
from collections import UserDict, namedtuple


# определяем базовую логику геттеров и сеттеров, которую потом можем переопределять в классах-наследниках
class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    # инициализация через родительский конструктор
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    # инициализация через родительский конструктор
    def __init__(self, phone):
        super().__init__(phone)

    # переопределяем сеттер родительского класса
    @Field.value.setter
    def value(self, new_value):
        try:
            # шаблон типа "либо 9 цифр подряд, либо 12 цифр подряд до конца строки"; "+" обрезаем в любом случае;
            # если нам дают номер в формате 9 цифро, добавляем код "380"
            new_value = re.search('(?:\d{9}\\b|\d{12}\\b)', new_value).group()
            new_value = new_value if len(new_value) == 12 else '380'+new_value

            # вызывем метод родительского класса через свойство fset аттрибута property
            Field.value.fset(self, new_value)
        except AttributeError:
            print('''Phone number have to be given either in a form "380*********" or in a form "*********", 
            without any non-digit symbols except '+'!''')

    def __repr__(self):
        return self.value if self.value else None


class Birthday(Field):
    # инициализация через родительский конструктор
    def __init__(self, date):
        super().__init__(date)

    # переопределяем сеттер родительского класса
    @Field.value.setter
    def value(self, new_value):
        try:
            new_value = re.search('\d{,2}/\d{,2}/\d{4}', new_value).group()
            date_items = [int(item) for item in new_value.split('/')]
            new_value = datetime(*reversed(date_items)).date()

            # вызывем метод родительского класса через свойство fset аттрибута property
            Field.value.fset(self, new_value)
        except AttributeError:
            print('Birthday date have to be given in a form "DD/MM/YYYY" or "D/M/YYYY" or "D/MM/YYYY" or "DD/M/YYYY"!')

    def __repr__(self):
        return self.value.strftime('%d %B %Y')


class Record:
    def __init__(self, name: Name, birthday=None):
        self.name = name
        self.birthday = birthday
        self.phone_list = []

    # на случай, если в запись передается несколько одинаковых объектов Phone,
    # конвертируем список телефонов в множество и обратно в список, чтобы убрать повторяющиеся объекты
    def add_phone(self, *phones):
        [self.phone_list.append(phone) for phone in phones]
        self.phone_list = list(set(self.phone_list))

    def get_phone_list(self):
        return list(map(lambda phone: phone.value, self.phone_list))

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        for phone in filter(lambda x: x.value == old_phone.value, self.phone_list):
            index = self.phone_list.index(phone)
            self.phone_list[index].value = new_phone.value

    def delete_phone(self, phone: Phone):
        for phone in list(filter(lambda x: x.value == phone.value, self.phone_list)):
            self.phone_list.remove(phone)

    def add_birthday(self, new_birthday: Birthday):
        self.birthday = new_birthday

    def days_to_birthday(self):
        try:
            now = datetime.now().date()
            nearest_bd = datetime(
                year=now.year, month=self.birthday.value.month, day=self.birthday.value.day).date()
            delta = nearest_bd - now

            if delta.days < 0:
                nearest_bd = nearest_bd.replace(year=nearest_bd.year+1)
                new_delta = nearest_bd - now
                return new_delta.days
            else:
                return f'{delta.days} days to the next birthday.'
        except AttributeError:
            print('No birthday date is given!')

    def __repr__(self):
        return (f'Name: {self.name.value}\n' +
                f'Phones: {[phone.value for phone in self.phone_list]}\n' +
                f'Birthday: {self.birthday}\n\n')

    def __str__(self):
        return self.__repr__()


class AdressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.iter_index = 0

    # можно сразу передавать несколько записей; если запись с таким именем уже существует, н едобавляем ее
    def add_record(self, *records):
        for record in records:
            key = record.name.value
            if key not in self.data:
                self.data[key] = record
            else:
                print(f'Record {key} already exists!')

    def get_record(self, name: Name):
        return self.data.get(name)

    # здесь просто возвращаем собъект, без ссылки на внутренний контейнер data; возможно благодаря тому, что переопределили
    # ниже метод __repr__, и объект имеет удобное отражение
    def get_all(self):
        return self

    def delete_record(self, *names):
        [self.data.pop(key) for key in names]

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
        for _ in range(n):
            try:
                list_of_data.append(next(self))
            except StopIteration:
                print('Data is over!')
                break

        return list_of_data

    def __repr__(self):
        string = f''
        for key, val in self.data.items():
            string += f'Record for name {key}:\n{val}'
        return string

    def __str__(self):
        return self.__repr__()
