from . import db
from sqlalchemy.ext.associationproxy import association_proxy


class Phone(db.Model):

    __tablename__ = 'phones'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('record.id', ondelete='CASCADE'))
    record = db.relationship('Record', back_populates='phones')

    def __repr__(self):
        return (f'ID: {self.id}\n' +
                f'Phone: {self.phone}.')


class Email(db.Model):

    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('record.id', ondelete='CASCADE'))
    record = db.relationship('Record', back_populates='emails')

    def __repr__(self):
        return (f'ID: {self.id}\n' +
                f'Email: {self.email}.')


class Birthday(db.Model):

    __tablename__ = 'birthday'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    birthday = db.Column(db.Date, nullable=True)
    records = db.relationship('Record', back_populates='birthday')

    def __init__(self, birthday):
        self.birthday = birthday if birthday else None

    def __repr__(self):
        return (f'ID: {self.id}\n' +
                f'Birthday: {self.birthday}.')


class Record_Address_Relationship(db.Model):

    __tablename__ = 'record_address'

    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('record.id'), primary_key=True)


class Address(db.Model):

    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(512), nullable=True)
    records = db.relationship('Record', secondary='record_address', back_populates='addresses')

    def __init__(self, address: str):
        self.address = address

    def __repr__(self):
        return (f'ID: {self.id}\n' +
                f'Address: {self.address}.')


class Record(db.Model):

    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    phones = db.relationship('Phone', back_populates='record', cascade='all, delete')
    emails = db.relationship('Email', back_populates='record', cascade='all, delete')
    addresses = db.relationship('Address', secondary='record_address', back_populates='records')
    birthday_id = db.Column(db.ForeignKey('birthday.id'))
    birthday = db.relationship('Birthday', back_populates='records')

    phones_val = association_proxy('phones', 'phone')
    emails_val = association_proxy('emails', 'email')
    addresses_val = association_proxy('addresses', 'address')
    birthday_val = association_proxy('birthday', 'birthday')

    def __repr__(self):
        return (f'ID : {self.id}\n' +
                f'Name: {self.name}\n' +
                f'Phones: {"; ".join(self.phones_val)}\n' +
                f'Emails: {"; ".join(self.emails_val)}\n' +
                f'Birthday: {self.birthday_val}\n' +
                f'Address: {chr(10).join(self.addresses_val)}.')

    def __str__(self):
    	return self.__repr__()