from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from create_connection import Base


class Name(Base):

    __tablename__ = 'names'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(56), unique=True, nullable=False)
    record_id = Column(Integer, ForeignKey('record.id', ondelete='CASCADE'))
    record = relationship('Record', back_populates='name',
                          cascade='all, delete')

    def __repr__(self):
        return (f'ID: {self.id}\n' +
                f'Name: {self.name}\n' +
                f'Record: {self.record.id}, {self.record.name_val}.')


class Phone(Base):

    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(20), unique=True, nullable=True)
    record_id = Column(Integer, ForeignKey('record.id', ondelete='CASCADE'))
    record = relationship('Record', back_populates='phones')

    def __repr__(self):
        return (f'ID: {self.id}\n' +
                f'Phone: {self.phone}.')


class Email(Base):

    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(320), unique=True, nullable=True)
    record_id = Column(Integer, ForeignKey('record.id', ondelete='CASCADE'))
    record = relationship('Record', back_populates='emails')

    def __repr__(self):
        return (f'ID: {self.id}\n' +
                f'Email: {self.email}.')


class Birthday(Base):

    __tablename__ = 'birthday'

    id = Column(Integer, primary_key=True, autoincrement=True)
    birthday = Column(Date, nullable=True)
    records = relationship('Record', back_populates='birthday')

    def __init__(self, birthday):
        self.birthday = birthday if birthday else None

    def __repr__(self):
        return (f'ID: {self.id}\n' +
                f'Birthday: {self.birthday}.')


class Record_Address_Relationship(Base):

    __tablename__ = 'record_address'

    address_id = Column(Integer, ForeignKey('address.id'), primary_key=True)
    record_id = Column(Integer, ForeignKey('record.id'), primary_key=True)


class Address(Base):

    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(512), nullable=True)
    records = relationship(
        'Record', secondary='record_address', back_populates='addresses')

    def __init__(self, address: str):
        self.address = address

    def __repr__(self):
        return (f'ID: {self.id}\n' +
                f'Address: {self.address}.')


class Record(Base):

    __tablename__ = 'record'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = relationship('Name', uselist=False,
                        back_populates='record', cascade='all, delete')
    phones = relationship(
        'Phone', back_populates='record', cascade='all, delete')
    emails = relationship(
        'Email', back_populates='record', cascade='all, delete')
    addresses = relationship(
        'Address', secondary='record_address', back_populates='records')
    birthday_id = Column(ForeignKey('birthday.id'))
    birthday = relationship('Birthday', back_populates='records')

    name_val = association_proxy('name', 'name')
    phones_val = association_proxy('phones', 'phone')
    emails_val = association_proxy('emails', 'email')
    addresses_val = association_proxy('addresses', 'address')
    birthday_val = association_proxy('birthday', 'birthday')

    def __repr__(self):
        return (f'ID : {self.id}\n' +
                f'Name: {self.name_val}\n' +
                f'Phones: {"; ".join(self.phones_val)}\n' +
                f'Emails: {"; ".join(self.emails_val)}\n' +
                f'Birthday: {self.birthday_val}\n' +
                f'Address: {chr(10).join(self.addresses_val)}.')
