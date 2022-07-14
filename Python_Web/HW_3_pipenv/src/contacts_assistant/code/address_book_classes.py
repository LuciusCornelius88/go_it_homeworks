import pickle
from collections import UserDict
from copy import deepcopy
from contacts_assistant.code.decorators import errors_handler
from contacts_assistant.code.abstract_methods import AddFields, DeleteFields, GetFields, SearchInFields, RepresentObjects
from contacts_assistant.code.exceptions import RecordAlreadyExistsError, RecordDoesNotExistError
from contacts_assistant.code.record_classes import Record, RecordCreator
from contacts_assistant.code.fields_creators import NameCreator


# -------------ADDRESS_BOOK-------------


class AddressBook(UserDict):

    def __init__(self, filepath):
        super().__init__()
        self.iterator = AddressBookIterator(self)
        self.serializer = SerializeAddressBook(self, filepath)

    @errors_handler
    def add_record(self) -> str:
        adder = AddRecord(self)
        adder.add()
        return 'Record was successfully added!'

    @errors_handler
    def delete_record(self) -> str:
        deleter = DeleteRecord(self)
        deleter.delete()
        return 'Record was successfully deleted!'

    @errors_handler
    def get_record(self) -> Record:
        getter = GetRecord(self)
        return getter.get()

    @errors_handler
    def find_soonest_bd(self) -> str:
        finder = FindSoonestBD(self)
        return finder.find_soonest_bd()

    def search_records(self) -> list:
        searcher = SearchRecord(self)
        return searcher.search()

    def show_all(self) -> str:
        return str(self) if self.data else 'There is no record yet in address book!'

    def save_to_file(self) -> str:
        self.serializer.update(self)
        self.serializer.serialize()
        return 'Address book was successfully saved to file!'

    def restore_from_file(self):
        return self.serializer.deserialize()

    @errors_handler
    def iterate(self) -> list:
        self.iterator.update(self)
        return self.iterator.iterate()

    def __repr__(self) -> str:
        representator = RepresentAddressBook(self)
        return representator.represent()

    def __str__(self) -> str:
        return self.__repr__()


# -------------METHODS_TO_HANDLE_FIELDS_IN_ADDRESS_BOOK-------------


# RecordAlreadyExistsException
# LoopInterruptionError
class AddRecord(AddFields):

    def __init__(self, address_book: AddressBook):
        self.address_book = address_book
        self.record_creator = RecordCreator()
        self.record = None

    def create_record(self) -> Record:
        self.record_creator.create_name()
        self.record_creator.create_phone()
        self.record_creator.create_email()
        self.record_creator.create_address()
        self.record_creator.create_birthday()
        return self.record_creator.get_record()

    def add(self):
        self.record = self.create_record()
        key = self.record.name.value
        if key in self.address_book.data:
            raise RecordAlreadyExistsError
        self.address_book.data[key] = self.record


# RecordDoesNotExistError(KeyError)
# LoopInterruptionError
class DeleteRecord(DeleteFields):

    def __init__(self, address_book: AddressBook):
        self.address_book = address_book
        self.name_creator = NameCreator()
        self.name = None

    def delete(self):
        self.name = self.name_creator.create()
        if self.name.value not in self.address_book.data:
            raise RecordDoesNotExistError
        del self.address_book.data[self.name.value]


# RecordDoesNotExistError(KeyError)
# LoopInterruptionError
class GetRecord(GetFields):

    def __init__(self, address_book: AddressBook):
        self.address_book = address_book
        self.name_creator = NameCreator()
        self.name = None

    def get(self):
        self.name = self.name_creator.create()
        if self.name.value not in self.address_book.data:
            raise RecordDoesNotExistError
        return self.address_book.data[self.name.value]


class SearchRecord(SearchInFields):

    def __init__(self, address_book: AddressBook):
        self.address_book = address_book
        self.string = input(
            'Please, enter string, you want records to match with: ')

    def search(self):
        list_of_records = []

        for record in self.address_book.data.values():
            list_of_attributes = []

            for attribute in record.__dict__.values():
                if isinstance(attribute, list):
                    [list_of_attributes.append(item) for item in attribute]
                elif not attribute:
                    continue
                else:
                    list_of_attributes.append(attribute)

            for item in list_of_attributes:
                if self.string.lower() in str(item.value).lower():
                    list_of_records.append(record)
                    break

        records_to_str = ''.join(
            map(lambda record: str(record), list_of_records))
        return records_to_str if records_to_str else 'No matches were found!'


# ValueError
class FindSoonestBD:

    def __init__(self, address_book: AddressBook):
        self.address_book = address_book
        self.days_till_bd = int(input(
            'Please, enter number of days of period, within that you want to find birthdays: '))

    def find_soonest_bd(self) -> str:
        records_with_bd = list(
            filter(lambda record: record.birthday.value, self.address_book.data.values()))
        records = list(filter(lambda record: record.days_to_birthday()
                       <= self.days_till_bd, records_with_bd))
        records_to_str = ''.join(map(lambda record: str(record), records))
        return records_to_str if records_to_str else 'No matches were found!'


class SerializeAddressBook:

    def __init__(self, address_book: AddressBook, filepath):
        self.address_book = address_book
        self.filepath = filepath

    def __deepcopy__(self, memo):
        copy_obj = AddressBook(self.filepath)
        memo[id(copy_obj)] = copy_obj
        copy_obj.data = deepcopy(self.address_book.data)
        return copy_obj

    def update(self, address_book: AddressBook):
        self.address_book = address_book

    def serialize(self):
        with open(self.filepath, 'w+b') as file:
            pickle.dump(self, file)

    def deserialize(self):
        with open(self.filepath, 'r+b') as file:
            return deepcopy(pickle.load(file))


# ValueError
class AddressBookIterator:

    def __init__(self, address_book: AddressBook):
        self.address_book = address_book
        self.iter_index = 0

    def update(self, address_book: AddressBook):
        self.address_book = address_book

    def __next__(self):
        keys = list(self.address_book.data.keys())
        if self.iter_index <= len(self.address_book.data)-1:
            self.iter_index += 1
            index = keys[self.iter_index-1]
            return self.address_book.data[index]
        else:
            self.iter_index = 0
        raise StopIteration

    def __iter__(self):
        return self

    def iterate(self) -> list:
        list_of_records = []
        n_iterations = int(
            input('Please, enter number of records, that are to be shown: '))

        for _ in range(n_iterations):
            try:
                list_of_records.append(next(self))
            except StopIteration:
                if not list_of_records and len(self.address_book.data) > 0:
                    list_of_records.append(next(self))
                    continue
                else:
                    break

        records_to_str = ''.join(
            map(lambda record: str(record), list_of_records))
        return records_to_str if records_to_str else 'There is no record yet in address book!'


class RepresentAddressBook(RepresentObjects):

    def __init__(self, address_book: AddressBook):
        self.address_book = address_book

    def represent(self) -> str:
        string = ''
        records = list(self.address_book.data.values())

        for record in records:
            string += f'{record}\n'

        return string
