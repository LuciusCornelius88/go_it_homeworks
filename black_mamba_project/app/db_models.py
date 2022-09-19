from . import db

#FINTECH_NEWS
class FintechNews(db.Model):

	__tablename__ = 'fintech_news'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	category = db.Column(db.String(128), nullable=True)
	title = db.Column(db.String(128), nullable=False)
	link = db.Column(db.String(512), nullable=False)
	published_on = db.Column(db.Date, nullable=True)
	language = db.Column(db.String(8), nullable=False)



#CURRENCY_IN_DIFFERENT_BANKS
class Currency_Bank(db.Model):

	__tablename__ = 'currency_bank'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
	bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'))


class Bank(db.Model):

	__tablename__ = 'bank'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	bank_name = db.Column(db.String(128), nullable=False)
	currencies = db.relationship('Currency', secondary='currency_bank', back_populates='banks')
	buy_values = db.relationship('BuyValues', back_populates='bank', cascade='all, delete')
	sale_values = db.relationship('SaleValues', back_populates='bank', cascade='all, delete')


class Currency(db.Model):

	__tablename__ = 'currency'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	currency_name = db.Column(db.String(128), nullable=False)
	banks = db.relationship('Bank', secondary='currency_bank', back_populates='currencies')
	buy_values = db.relationship('BuyValues', back_populates='currency', cascade='all, delete')
	sale_values = db.relationship('SaleValues', back_populates='currency', cascade='all, delete')
	

class BuyValues(db.Model):

	__tablename__ = 'buy_values'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	bank_id = db.Column(db.Integer, db.ForeignKey('bank.id', ondelete='CASCADE'))
	bank = db.relationship('Bank', back_populates='buy_values')
	currency_id = db.Column(db.Integer, db.ForeignKey('currency.id', ondelete='CASCADE'))
	currency = db.relationship('Currency', back_populates='buy_values')
	buy_value = db.Column(db.Float, nullable=False)
	date_of = db.Column(db.Date, nullable=False)


class SaleValues(db.Model):

	__tablename__ = 'sale_values'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	bank_id = db.Column(db.Integer, db.ForeignKey('bank.id', ondelete='CASCADE'))
	bank = db.relationship('Bank', back_populates='sale_values')
	currency_id = db.Column(db.Integer, db.ForeignKey('currency.id', ondelete='CASCADE'))
	currency = db.relationship('Currency', back_populates='sale_values')
	sale_value = db.Column(db.Float, nullable=False)
	date_of = db.Column(db.Date, nullable=False)
