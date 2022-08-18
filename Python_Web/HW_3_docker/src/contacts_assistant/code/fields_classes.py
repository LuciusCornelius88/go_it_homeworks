from datetime import datetime


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

    @Field.value.setter
    def value(self, new_value):
        Field.value.fset(self, new_value.strip())

    def __repr__(self):
        return f'Name: {self.value}'

    def __str__(self):
        return self.__repr__()


class Phone(Field):
    def __init__(self, phone: str):
        super().__init__(phone)

    @Field.value.setter
    def value(self, new_value):
        Field.value.fset(self, new_value)

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.__repr__()


class Email(Field):
    def __init__(self, email: str):
        super().__init__(email)

    @Field.value.setter
    def value(self, new_value):
        Field.value.fset(self, new_value)

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.__repr__()


class Address(Field):
    def __init__(self, address: list):
        super().__init__(address)

    @Field.value.setter
    def value(self, new_value):
        Field.value.fset(self, new_value)

    def create_representation(self):
        string = ''
        for item in self.value:
            if self.value.index(item) == 0:
                string += 'Address: {:<5}\n'.format(item)
            elif self.value.index(item) == len(self.value)-1:
                string += (' ')*len('Address: ') + '{:<5}'.format(item)
            else:
                string += (' ')*len('Address: ') + '{:<5}\n'.format(item)
        return string

    def __repr__(self):
        if self.value:
            return self.create_representation()
        else:
            return 'Address: No address!'

    def __str__(self):
        return self.__repr__()


class Birthday(Field):
    def __init__(self, date: list):
        super().__init__(date)

    @Field.value.setter
    def value(self, new_value):
        new_value = datetime(*new_value).date() if new_value else []
        Field.value.fset(self, new_value)

    def __repr__(self):
        main_part = self.value.strftime(
            '%d %B %Y') if self.value else 'No birthday!'
        return f'Birthday: {main_part}'

    def __str__(self):
        return self.__repr__()
