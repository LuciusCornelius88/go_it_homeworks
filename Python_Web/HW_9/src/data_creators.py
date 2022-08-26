from abc import ABC, abstractmethod
from parsers import AddressItems, NameParser, PhoneParser, EmailParser, AddressParser, BirthdayParser
from decorators import errors_handler, loop_interruption_decorator

from datetime import datetime


class FieldsCreator(ABC):

    @abstractmethod
    def create(self):
        pass


class BirthdayCreator(FieldsCreator):

    def __init__(self):
        self.default_value = [1900, 1, 1]
        self.parser = BirthdayParser()

    @errors_handler
    def birthday_creator(self):
        input_date = input(
            'Enter birthday or enter "***" to set birthday to default value or enter "###" to exit the loop: ')
        if input_date == '###':
            return None
        if input_date == '***':
            self.parser.string = ';'.join(
                map(lambda date_item: str(date_item), self.default_value[::-1]))
        else:
            self.parser.string = input_date
        return self.parser.parse_string()

    @loop_interruption_decorator
    def create(self):
        birthday = self.birthday_creator()
        return datetime(*birthday).date() if birthday else None


class AddressCreator(FieldsCreator):

    def __init__(self):
        self.address_items = []
        self.parser = AddressParser(AddressItems)
        self.delim = ': '

    @errors_handler
    def city_creator(self) -> str:
        city = input(
            'Enter your city or enter "***" to set city name to default value or enter "###" to exit the loop: ')
        if city == '###':
            return None
        if city == '***':
            city = AddressItems.CITY.value.lower()
        self.parser.string = city = AddressItems.CITY.value + self.delim + city
        city = self.parser.parse_string(AddressItems.CITY)
        return city

    @errors_handler
    def street_creator(self) -> str:
        street = input(
            'Enter street or enter "***" to set street to default value or enter "###" to exit the loop: ')
        if street == '###':
            return None
        if street == '***':
            street = AddressItems.STREET.value.lower()
        self.parser.string = street = AddressItems.STREET.value + self.delim + street
        street = self.parser.parse_string(AddressItems.STREET)
        return street

    @errors_handler
    def house_number_creator(self) -> str:
        house = input(
            'Enter your house or enter "***" to set house to default value or enter "###" to exit the loop: ')
        if house == '###':
            return None
        if house == '***':
            house = AddressItems.HOUSE.value.lower()
        self.parser.string = house = AddressItems.HOUSE.value + self.delim + house
        house = self.parser.parse_string(AddressItems.HOUSE)
        return house

    @errors_handler
    def appartament_creator(self) -> str:
        appartament = input(
            'Enter your flat or enter "***" to set flat to default value or enter "###" to exit the loop: ')
        if appartament == '###':
            return None
        if appartament == '***':
            appartament = AddressItems.APPARTAMENT.value.lower()
        self.parser.string = appartament = AddressItems.APPARTAMENT.value + \
            self.delim + appartament
        appartament = self.parser.parse_string(AddressItems.APPARTAMENT)
        return appartament

    @errors_handler
    def zip_code_creator(self) -> str:
        zip_code = input(
            'Enter your zip or enter "***" to set zip to default value or enter "###" to exit the loop: ')
        if zip_code == '###':
            return None
        if zip_code == '***':
            zip_to_ord = [ord(i) for i in AddressItems.ZIP.value.lower()]
            zip_code = ''.join(
                list(map(lambda zip_item: str(zip_item), zip_to_ord)))
        self.parser.string = zip_code = AddressItems.ZIP.value + self.delim + zip_code
        zip_code = self.parser.parse_string(AddressItems.ZIP)
        return zip_code

    @loop_interruption_decorator
    def create_city(self) -> str:
        return self.city_creator()

    @loop_interruption_decorator
    def create_street(self) -> str:
        return self.street_creator()

    @loop_interruption_decorator
    def create_house_number(self) -> str:
        return self.house_number_creator()

    @loop_interruption_decorator
    def create_appartament(self) -> str:
        return self.appartament_creator()

    @loop_interruption_decorator
    def create_zip_code(self) -> str:
        return self.zip_code_creator()

    def create(self) -> list:
        self.address_items.append(self.create_city())
        self.address_items.append(self.create_street())
        self.address_items.append(self.create_house_number())
        self.address_items.append(self.create_appartament())
        self.address_items.append(self.create_zip_code())
        return '; '.join(self.address_items)


class NameCreator(FieldsCreator):

    def __init__(self):
        self.parser = NameParser()
        self.default_value = 'Name'

    @errors_handler
    def name_creator(self):
        input_name = input(
            'Please, enter name or enter "***" to set name to default value or enter "###" to exit the loop: ')
        if input_name == '###':
            return None
        elif input_name == '***':
            self.parser.string = self.default_value
        else:
            self.parser.string = input_name
        return self.parser.parse_string()

    @loop_interruption_decorator
    def create(self) -> str:
        name = self.name_creator()
        return name


class PhoneCreator(FieldsCreator):

    def __init__(self):
        self.parser = PhoneParser()
        self.default_value = '000000000000'

    @errors_handler
    def phone_creator(self):
        input_phone = input(
            'Enter phone or enter "***" to set phone to default value or enter "###" to exit the loop: ')
        if input_phone == '###':
            return None
        if input_phone == '***':
            self.parser.string = self.default_value
        else:
            self.parser.string = input_phone
        return self.parser.parse_string()

    @loop_interruption_decorator
    def create(self) -> str:
        phone = self.phone_creator()
        return phone


class EmailCreator(FieldsCreator):

    def __init__(self):
        self.parser = EmailParser()
        self.default_value = 'some_email@com'

    @errors_handler
    def email_creator(self):
        input_email = input(
            'Enter email or enter "***" to set email to default value or enter "###" to exit the loop: ')
        if input_email == '###':
            return None
        if input_email == '***':
            self.parser.string = self.default_value
        else:
            self.parser.string = input_email
        return self.parser.parse_string()

    @loop_interruption_decorator
    def create(self) -> str:
        email = self.email_creator()
        return email
