from flask import render_template, request, redirect
from flask import current_app as app
from ..db_models import *



# ------------------Filter_by_bank------------------

@app.route('/currency/get_by_bank/', strict_slashes=False)
def get_values_by_bank():
	banks = db.session.query(Bank).all()
	return render_template('currency_templates/choose_bank.html', banks=banks)


@app.route('/currency/filter_by_bank/', methods=['POST'], strict_slashes=False)
def filter_by_bank():
	name = request.form.get('bank')
	bank = db.session.query(Bank).filter_by(bank_name=name).first()
	currencies = bank.currencies
	values = {}

	for currency in currencies:
		buy_value_obj = db.session.query(BuyValues).filter((BuyValues.bank_id == bank.id) & 
													   (BuyValues.currency_id == currency.id)).first()
		sale_value_obj = db.session.query(SaleValues).filter((SaleValues.bank_id == bank.id) & 
													     (SaleValues.currency_id == currency.id)).first()
		
		buy_value = buy_value_obj.buy_value
		sale_value = sale_value_obj.sale_value
		date_of = buy_value_obj.date_of
		
		values[currency.currency_name] = [buy_value, sale_value, date_of]

	return render_template('currency_templates/currency_output.html', name=name, values=values)



# ------------------Filter_by_currency------------------

@app.route('/currency/get_by_currency/', strict_slashes=False)
def get_values_by_currency():
	currencies = db.session.query(Currency).all()
	return render_template('currency_templates/choose_currency.html', currencies=currencies)


@app.route('/currency/filter_by_currency/', methods=['POST'], strict_slashes=False)
def filter_by_currency():
	name = request.form.get('currency')
	currency = db.session.query(Currency).filter_by(currency_name=name).first()
	banks = currency.banks
	values = {}

	for bank in banks:
		buy_value_obj = db.session.query(BuyValues).filter((BuyValues.bank_id == bank.id) & 
													   (BuyValues.currency_id == currency.id)).first()
		sale_value_obj = db.session.query(SaleValues).filter((SaleValues.bank_id == bank.id) & 
													     (SaleValues.currency_id == currency.id)).first()

		buy_value = buy_value_obj.buy_value
		sale_value = sale_value_obj.sale_value
		date_of = buy_value_obj.date_of

		values[bank.bank_name] = [buy_value, sale_value, date_of]

	return render_template('currency_templates/currency_output.html', name=name, values=values)



# ------------------Filter_by_bank_and_currency------------------

@app.route('/currency/get_by_bank_and_currency/', strict_slashes=False)
def get_values_by_bank_and_currency():
	banks = db.session.query(Bank).all()
	currencies = db.session.query(Currency).all()
	return render_template('currency_templates/choose_bank_and_currency.html', banks=banks, currencies=currencies)


@app.route('/currency/filter_by_bank_and_currency/', methods=['POST'], strict_slashes=False)
def filter_by_bank_and_currency():
	bank_name = request.form.get('bank')
	currency_name = request.form.get('currency')

	bank = db.session.query(Bank).filter_by(bank_name=bank_name).first()
	currency = db.session.query(Currency).filter_by(currency_name=currency_name).first()

	values = {}

	buy_value_obj = db.session.query(BuyValues).filter((BuyValues.bank_id == bank.id) & 
												   (BuyValues.currency_id == currency.id)).first()
	sale_value_obj = db.session.query(SaleValues).filter((SaleValues.bank_id == bank.id) & 
												     (SaleValues.currency_id == currency.id)).first()

	name = f'{bank.bank_name} {currency.currency_name}'

	try:
		buy_value = buy_value_obj.buy_value
		sale_value = sale_value_obj.sale_value
		date_of = buy_value_obj.date_of
	except:
		buy_value = 'N/A'
		sale_value = 'N/A'
		date_of = 'N/A'

	values[name] = [buy_value, sale_value, date_of]

	return render_template('currency_templates/currency_output.html', name=name, values=values)



# ------------------Deleter------------------

@app.route('/currency/delete_all_data/', strict_slashes=False)
def currency_delete_all():
	db.session.query(Currency_Bank).delete()
	db.session.commit()
	
	db.session.query(Bank).delete()
	db.session.query(Currency).delete()
	db.session.query(BuyValues).delete()
	db.session.query(SaleValues).delete()

	db.session.commit()

	return render_template('data_deleted.html')


