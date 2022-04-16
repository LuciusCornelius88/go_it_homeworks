import re
from datetime import datetime

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
    def __init__(self, name: str):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone: str):
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
    def __init__(self, date: str):
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

    def __str__(self):
        return self.__repr__()
