from datetime import datetime
from contacts_assistant.code.decorators import errors_handler
from contacts_assistant.code.fields_creators import NameCreator, PhoneCreator, EmailCreator, \
    AddressCreator, DateCreator
from contacts_assistant.code.exceptions import PhoneAlreadyExistsError, EmailAlreadyExistsError, \
    PhoneDoesNotExistError, EmailDoesNotExistError
from contacts_assistant.code.abstract_methods import *


class Record:

    def __init__(self):
        self.name = None
        self.address = None
        self.birthday = None
        self.phone_list = []
        self.email_list = []

    @errors_handler
    def add_phone(self) -> str:
        adder = AddPhone(self)
        return adder.add()

    @errors_handler
    def add_email(self) -> str:
        adder = AddEmail(self)
        return adder.add()

    @errors_handler
    def change_phone(self) -> str:
        changer = ChangePhone(self)
        return changer.change()

    @errors_handler
    def change_email(self) -> str:
        changer = ChangeEmail(self)
        return changer.change()

    def change_address(self) -> str:
        changer = ChangeAddress(self)
        return changer.change()

    def change_birthday(self) -> str:
        changer = ChangeBirthday(self)
        return changer.change()

    @errors_handler
    def delete_phone(self) -> str:
        deleter = DeletePhone(self)
        return deleter.delete()

    @errors_handler
    def delete_email(self) -> str:
        deleter = DeleteEmail(self)
        return deleter.delete()

    def delete_address(self) -> str:
        deleter = DeleteAddress(self)
        return deleter.delete()

    def delete_birthday(self) -> str:
        deleter = DeleteBirthday(self)
        return deleter.delete()

    def days_to_birthday(self) -> int:
        searcher = SearchBirthday(self)
        return searcher.search()

    def __repr__(self) -> str:
        representator = RepresentRecord(self)
        return representator.represent()

    def __str__(self) -> str:
        return self.__repr__()


# -------------ADDERS-------------


# PhoneAlreadyExistsError
# LoopInterruptionError
class AddPhone(AddFields):

    def __init__(self, record: Record):
        self.record = record
        self.phone_creator = PhoneCreator()
        self.phone = None

    def add(self):
        self.phone = self.phone_creator.create()
        if self.phone.value in list(map(lambda phone: phone.value, self.record.phone_list)):
            raise PhoneAlreadyExistsError
        self.record.phone_list.append(self.phone)
        return f'New phone was added for record {self.record.name.value.upper()}'


# EmailAlreadyExistsError
# LoopInterruptionError
class AddEmail(AddFields):

    def __init__(self, record: Record):
        self.record = record
        self.email_creator = EmailCreator()
        self.email = None

    def add(self):
        self.email = self.email_creator.create()
        if self.email.value in list(map(lambda email: email.value, self.record.email_list)):
            raise EmailAlreadyExistsError
        self.record.email_list.append(self.email)
        return f'New email was added for record {self.record.name.value.upper()}'


# -------------CHANGERS-------------

# PhoneDoesNotExistError
# LoopInterruptionError
class ChangePhone(ChangeFields):

    def __init__(self, record: Record):
        self.record = record
        self.phone_creator = PhoneCreator()
        self.old_phone = None
        self.new_phone = None
        self.return_string = None

    def redefine_attrs(self):
        self.old_phone = self.old_phone_setter()
        print(f'Old phone: {self.old_phone.value}')
        self.new_phone = self.phone_creator.create()
        print(f'New phone: {self.new_phone.value}')
        self.return_string = (f'Phone {self.old_phone.value} was replaced with phone {self.new_phone.value} ' +
                              f'for record {self.record.name.value.upper()}.')

    def old_phone_setter(self):
        old_phone = self.phone_creator.create()
        phone_matched = list(
            filter(lambda phone: phone.value == old_phone.value, self.record.phone_list))
        if not phone_matched:
            raise PhoneDoesNotExistError
        return phone_matched[0]

    def change(self):
        self.redefine_attrs()
        index = self.record.phone_list.index(self.old_phone)
        self.record.phone_list[index].value = self.new_phone.value
        return self.return_string


# EmailDoesNotExistError
# LoopInterruptionError
class ChangeEmail(ChangeFields):

    def __init__(self, record: Record):
        self.record = record
        self.email_creator = EmailCreator()
        self.old_email = None
        self.new_email = None
        self.return_string = None

    def redefine_attrs(self):
        self.old_email = self.old_email_setter()
        print(f'Old email: {self.old_email.value}')
        self.new_email = self.email_creator.create()
        print(f'New email: {self.new_email.value}')
        self.return_string = (f'Email {self.old_email.value} was replaced with email {self.new_email.value} ' +
                              f'for record {self.record.name.value.upper()}.')

    def old_email_setter(self):
        old_email = self.email_creator.create()
        email_matched = list(
            filter(lambda email: email.value == old_email.value, self.record.email_list))
        if not email_matched:
            raise EmailDoesNotExistError
        return email_matched[0]

    def change(self):
        self.redefine_attrs()
        index = self.record.email_list.index(self.old_email)
        self.record.email_list[index].value = self.new_email.value
        return self.return_string


# LoopInterruptionError
class ChangeAddress(ChangeFields):

    def __init__(self, record: Record):
        self.record = record
        self.address_creator = AddressCreator()

    def change(self):
        self.record.address = self.address_creator.create()
        return f'New address was set for record {self.record.name.value.upper()}.'


# LoopInterruptionError
class ChangeBirthday(ChangeFields):

    def __init__(self, record: Record):
        self.record = record
        self.birthday_creator = DateCreator()

    def change(self):
        self.record.birthday = self.birthday_creator.create()
        return f'New birthday was set for record {self.record.name.value.upper()}.'


# -------------DELETERS-------------

# PhoneDoesNotExistError
# LoopInterruptionError
class DeletePhone(DeleteFields):

    def __init__(self, record: Record):
        self.record = record
        self.phone_creator = PhoneCreator()
        self.phone = None

    def delete(self):
        self.phone = self.phone_creator.create()
        phone_matched = list(
            filter(lambda phone: phone.value == self.phone.value, self.record.phone_list))
        if not phone_matched:
            raise PhoneDoesNotExistError
        self.record.phone_list.remove(phone_matched[0])
        return f'Phone {self.phone.value} in record {self.record.name.value.upper()} was succesfully deleted.'


# EmailDoesNotExistError
# LoopInterruptionError
class DeleteEmail(DeleteFields):

    def __init__(self, record: Record):
        self.record = record
        self.email_creator = EmailCreator()
        self.email = None

    def delete(self):
        self.email = self.email_creator.create()
        email_matched = list(
            filter(lambda email: email.value == self.email.value, self.record.email_list))
        if not email_matched:
            raise EmailDoesNotExistError
        self.record.email_list.remove(email_matched[0])
        return f'Email {self.email.value} in record {self.record.name.value.upper()} was succesfully deleted.'


class DeleteAddress(DeleteFields):

    def __init__(self, record: Record):
        self.record = record

    def delete(self):
        self.record.address.value = []
        return f'Address in record {self.record.name.value.upper()} was succesfully deleted.'


class DeleteBirthday(DeleteFields):

    def __init__(self, record: Record):
        self.record = record

    def delete(self):
        self.record.birthday.value = []
        return f'Birthday in record {self.record.name.value.upper()} was succesfully deleted.'


# -------------SEARCHERS-------------

# AttributeError
class SearchBirthday(SearchInFields):

    def __init__(self, record: Record):
        self.record = record

    def search(self) -> int:
        now = datetime.now().date()
        year = now.year
        month = self.record.birthday.value.month
        day = self.record.birthday.value.day
        nearest_bd = datetime(year=year, month=month, day=day).date()
        delta = nearest_bd - now

        if delta.days < 0:
            nearest_bd = nearest_bd.replace(year=nearest_bd.year+1)
            delta = nearest_bd - now

        return delta.days

# -------------REPRESENTERS-------------


class RepresentRecord(RepresentObjects):

    def __init__(self, record: Record):
        self.record = record
        self.phones = self.represent_phone_list()
        self.emails = self.represent_email_list()

    def represent_phone_list(self) -> str:
        phones = 'Phones: '
        for phone in self.record.phone_list:
            if self.record.phone_list.index(phone) == 0 and len(self.record.phone_list) > 1:
                phones += '{:<5}\n'.format(str(phone))
            elif self.record.phone_list.index(phone) == 0 and len(self.record.phone_list) <= 1:
                phones += '{:<5}'.format(str(phone))
            elif self.record.phone_list.index(phone) == len(self.record.phone_list)-1:
                phones += (' ')*len(phones) + '{:<5}'.format(str(phone))
            else:
                phones += (' ')*len(phones) + '{:<5}\n'.format(str(phone))
        return phones

    def represent_email_list(self) -> str:
        emails = 'Emails: '
        for email in self.record.email_list:
            if self.record.email_list.index(email) == 0 and len(self.record.email_list) > 1:
                emails += '{:<5}\n'.format(str(email))
            elif self.record.email_list.index(email) == 0 and len(self.record.email_list) <= 1:
                emails += '{:<5}'.format(str(email))
            elif self.record.email_list.index(email) == len(self.record.email_list)-1:
                emails += (' ')*len(emails) + '{:<5}'.format(str(email))
            else:
                emails += (' ')*len(emails) + '{:<5}\n'.format(str(email))

        return emails

    def create_title(self):
        string = ''
        title = f'|Record for name {self.record.name.value.upper()}:|\n'
        spaces = '|' + ' ' * (len(title)-3) + '|\n'
        upper_dash = ' ' + '_' * (len(title)-3) + '\n'
        lower_dash = '|' + '_' * (len(title)-3) + '|\n\n'
        string += upper_dash + spaces + title + lower_dash

        return string

    def represent(self) -> str:
        title = self.create_title()

        record_represantation = (f'{self.record.name}\n\n' +
                                 f'{self.phones}\n\n' +
                                 f'{self.emails}\n\n' +
                                 f'{self.record.address}\n\n' +
                                 f'{self.record.birthday}\n')
        return title + record_represantation


# -------------CREATOR-------------

class RecordCreator:

    def __init__(self):
        self.__record = Record()
        self.name_creator = NameCreator()
        self.phone_creator = PhoneCreator()
        self.email_creator = EmailCreator()
        self.address_creator = AddressCreator()
        self.birthday_creator = DateCreator()

    def create_name(self):
        self.__record.name = self.name_creator.create()

    def create_phone(self):
        phone = self.phone_creator.create()
        self.__record.phone_list.append(phone)

    def create_email(self):
        email = self.email_creator.create()
        self.__record.email_list.append(email)

    def create_address(self):
        self.__record.address = self.address_creator.create()

    def create_birthday(self):
        self.__record.birthday = self.birthday_creator.create()

    def get_record(self) -> Record:
        return self.__record
