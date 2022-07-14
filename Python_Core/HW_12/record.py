from fields import*


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

    def change_birthday(self, new_birthday: Birthday):
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
