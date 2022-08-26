from create_connection import session
from sqlalchemy.orm import contains_eager
from sqlalchemy import and_

from datetime import datetime, timedelta

from decorators import errors_handler
from exceptions import PhoneAlreadyExistsError, PhoneDoesNotExistError, EmailAlreadyExistsError, EmailDoesNotExistError, \
    RecordDoesNotExistError, RecordAlreadyExistsError, AddressAlreadyExistsError, AddressDoesNotExistError
from data_creators import BirthdayCreator, AddressCreator, NameCreator, PhoneCreator, EmailCreator
from db_models import Name, Phone, Email, Birthday, Address, Record, Record_Address_Relationship


def get_record():

    print('Get record_name.')
    record_name = NameCreator().create()
    record = session.query(Record).filter(
        Record.name.has(name=record_name)).first()
    if record:
        return record
    else:
        raise RecordDoesNotExistError


# AttributeError
def change_name():

    record = get_record()

    print('Create new name.')
    new_name = NameCreator().create()

    if session.query(Name).filter(Name.name == new_name).all():
        raise RecordAlreadyExistsError
    else:
        record.name_val = new_name
        session.commit()

    return(f'Name for record {record.id} was changed to {new_name}.')


# AttributeError
def add_phone():

    record = get_record()

    print('Create new phone.')
    new_phone = PhoneCreator().create()

    if session.query(Phone).filter(and_(Phone.phone == new_phone, Phone.record_id == record.id)).scalar():
        raise PhoneAlreadyExistsError
    else:
        session.add(Phone(phone=new_phone, record_id=record.id))
        session.commit()

    return f'Phone {new_phone} was added to record {record.id}.'


# AttributeError
def change_phone():

    record = get_record()

    print('Get old phone.')
    old_phone = PhoneCreator().create()

    print('Create new phone.')
    new_phone = PhoneCreator().create()

    phone = session.query(Phone).filter(
        and_(Phone.record_id == record.id, Phone.phone == old_phone)).scalar()

    if phone:
        phone.phone = new_phone
        session.commit()
    else:
        raise PhoneDoesNotExistError

    return f'Phone {old_phone} was replaced with phone {new_phone} for record {record.id}.'


# AttributeError
def delete_phone():

    record = get_record()

    print('Get old phone.')
    old_phone = PhoneCreator().create()

    phone = session.query(Phone).filter(
        and_(Phone.record_id == record.id, Phone.phone == old_phone)).scalar()

    if phone:
        session.delete(phone)
        session.commit()
    else:
        raise PhoneDoesNotExistError

    return f'Phone {old_phone} was deleted for record {record.id}.'


# AttributeError
def add_email():

    record = get_record()

    print('Create new email.')
    new_email = EmailCreator().create()

    if session.query(Email).filter(and_(Email.email == new_email, Email.record_id == record.id)).scalar():
        raise EmailAlreadyExistsError
    else:
        session.add(Email(email=new_email, record_id=record.id))
        session.commit()

    return f'Email {new_email} was added to record {record.id}.'


# AttributeError
def change_email():

    record = get_record()

    print('Get old email.')
    old_email = EmailCreator().create()

    print('Create new email.')
    new_email = EmailCreator().create()

    email = session.query(Email).filter(
        and_(Email.record_id == record.id, Email.email == old_email)).scalar()

    if email:
        email.email = new_email
        session.commit()
    else:
        raise EmailDoesNotExistError

    return f'Email {old_email} was replaced with email {new_email} for record {record.id}.'


# AttributeError
def delete_email():

    record = get_record()

    print('Get old email.')
    old_email = EmailCreator().create()

    email = session.query(Email).filter(
        and_(Email.record_id == record.id, Email.email == old_email)).scalar()

    if email:
        session.delete(email)
        session.commit()
    else:
        raise EmailDoesNotExistError

    return f'Email {old_email} was deleted for record {record.id}.'


# AttributeError
def add_address():

    record = get_record()

    print('Create new address.')
    new_address = AddressCreator().create()

    address = Address(new_address)

    if session.query(Address).filter(and_(Address.address == address.address,
                                          Address.records.any(id=record.id))).scalar():
        raise AddressAlreadyExistsError
    else:
        session.add(address)
        session.commit()

        record_to_address = Record_Address_Relationship(
            address_id=address.id, record_id=record.id)
        session.add(record_to_address)
        session.commit()

    return f'New address {address.id} was added to record {record.id}.'


# AttributeError
def change_address():

    record = get_record()

    print('Get old address.')
    old_address = AddressCreator().create()

    print('Create new address.')
    new_address = AddressCreator().create()

    address = session.query(Address).filter(and_(Address.records.any(id=record.id)),
                                            Address.address == old_address).scalar()

    if address:
        if session.query(Address).filter(and_(Address.address == address.address,
                                              Address.records.any(id=record.id))).scalar():
            raise AddressAlreadyExistsError

        else:
            address.address = new_address
            session.commit()
    else:
        raise AddressDoesNotExistError

    return f'Address {address.id} was changed for record {record.id}.'


# AttributeError
def delete_address():

    record = get_record()

    print('Get old address.')
    old_address = AddressCreator().create()

    address = session.query(Address).filter(and_(Address.records.any(id=record.id)),
                                            Address.address == old_address).scalar()

    if address:
        session.delete(address)
        session.commit()
    else:
        raise AddressDoesNotExistError

    return f'Address {address.id} was deleted for record {record.id}.'


# AttributeError
def change_birthday():

    record = get_record()

    print('Create new birthday.')
    new_birthday = BirthdayCreator().create()

    record.birthday_val = new_birthday
    session.commit()

    return f'Birthday {record.birthday_id} was changed for record {record.id}.'


# AttributeError
def delete_birthday():

    record = get_record()

    birthday = session.query(Birthday).filter(
        Birthday.records.any(id=record.id)).scalar()

    session.delete(birthday)
    session.commit()

    return f'Birthday {birthday.id} was deleted for record {record.id}.'


def add_record():

    def get_birthday_data():
        return BirthdayCreator().create()

    def get_address_data():
        return AddressCreator().create()

    def get_name_data():
        new_name = NameCreator().create()
        if session.query(Name).filter(Name.name == new_name).all():
            raise RecordAlreadyExistsError
        else:
            return new_name

    def get_phone_data():
        new_phone = PhoneCreator().create()
        if session.query(Phone).filter(Phone.phone == new_phone).all():
            raise PhoneAlreadyExistsError
        else:
            return new_phone

    def get_email_data():
        new_email = EmailCreator().create()
        if session.query(Email).filter(Email.email == new_email).all():
            raise EmailAlreadyExistsError
        else:
            return new_email

    def create_record():
        birthday = Birthday(get_birthday_data())
        address = Address(get_address_data())
        session.add_all([birthday, address])
        session.commit()

        record = Record(birthday_id=birthday.id)
        session.add(record)
        session.commit()

        record_to_address = Record_Address_Relationship(
            address_id=address.id, record_id=record.id)
        session.add(record_to_address)
        session.commit()

        return record

    @errors_handler
    def create_unique(record):
        name = Name(name=get_name_data(), record_id=record.id)
        phone = Phone(phone=get_phone_data(), record_id=record.id)
        email = Email(email=get_email_data(), record_id=record.id)

        session.add_all([name, phone, email])
        session.commit()

    @errors_handler
    def add():
        record = create_record()
        create_unique(record)
        return f'Record {record.id}: {record.name_val} was added.'

    return add()


def birthday_soon():
    n_days = int(input(
        'Please, enter number of days of period, within that you want to find birthdays: '))

    now_date = datetime.now().date()
    now_year = now_date.year
    lim_date = now_date + timedelta(days=n_days)

    birthdays = [i for i in session.query(Birthday.id, Birthday.birthday).all()
                 if (datetime(year=now_year, month=i.birthday.month, day=i.birthday.day).date() <= lim_date)]

    records = list(filter(None, [session.query(Record).filter(
        Record.birthday_id == bd.id).scalar() for bd in birthdays]))

    return records


def delete_record():

    record = get_record()
    session.delete(record)
    session.commit()

    return f'Record {record.id} was deleted.'


def show_n_records():

    n_records = int(input('How many records would you like me to show: '))

    records = session.query(Record).join(Record.name).options(contains_eager(Record.name)). \
        order_by(Name.name).limit(n_records).all()
    return records


def show_all():

    records = session.query(Record).all()
    return records if records else 'There is no record in database now!'


def delete_none():

    records = session.query(Record).filter(Record.name == None).all()
    for rec in records:
        session.delete(rec)
    session.commit()

    return 'Records without name were deleted.'


# @errors_handler
# def main():
    # print(change_name())

    # add_phone()
    # change_phone()
    # delete_phone()

    # add_email()
    # change_email()
    # delete_email()

    # add_address()
    # change_address()
    # delete_address()

    # change_birthday()
    # print(delete_birthday())

    # get_record()
    # add_record()
    # print(delete_record())

    # birthday_soon()
    # show_all()
    # print(show_n_records())

    # delete_none()

    # print(session.query(Record).all())

# if __name__ == '__main__':
# 	main()
