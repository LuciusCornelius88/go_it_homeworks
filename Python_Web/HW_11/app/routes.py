from flask import render_template, request, redirect
from flask import current_app as app
from datetime import datetime
from .db_models import db, Phone, Email, Birthday, Address, Record, Record_Address_Relationship


# ==================Secondary methods==================


def check_record(name):

	try:
		record = Record.query.filter_by(name=name).first_or_404()
		return record
	except Exception as e:
		return f'Error {e.code}: record with name {name} does not exist!'



def check_address(record, address_val):

	try:
		address = Address.query.filter((Address.records.any(id=record.id))&(Address.address == address_val)).first_or_404()
		return address
	except Exception as e:
		return f'Record {record.id} {record.name} does not have such address.'



def check_phone(record, phone_val):
	
	try:
		phone = Phone.query.filter((Phone.phone == phone_val)&(Phone.record_id == record.id)).first_or_404()
		return phone
	except Exception as e:
		return f'Error {e.code}: record {record.id} {record.name} does not have phone {phone_val}!'



def check_email(record, email_val):
	
	try:
		email = Email.query.filter((Email.email == email_val)&(Email.record_id == record.id)).first_or_404()
		return email
	except Exception as e:
		return f'Error {e.code}: record {record.id} {record.name} does not have email {email_val}!'



def create_address(request_form, keys):

	city = request_form.get(keys[0])
	street = request_form.get(keys[1])
	postal_code = request_form.get(keys[2])

	if ''.join([city, street, postal_code]):
		return ', '.join([city, street, postal_code])
	else:
		return ''



def create_birthday(request_form):

	try:
		day = int(request_form.get('day'))
		month = int(request_form.get('month'))
		year = int(request_form.get('year'))
		return datetime(year, month, day).date()
	except ValueError:
		return None


# ==================Primary methods==================

# -----------------Main page handlers----------------

@app.route('/', strict_slashes=False)
def index():
	records = db.session.query(Record).all()
	return render_template('index.html', records=records)



@app.route('/detail/<string:name>', strict_slashes=False)
def detail(name):
	record = Record.query.filter_by(name=name).first()
	return render_template("detail.html", record=record)



@app.route('/add', strict_slashes=False)
def add():
	return render_template('record.html')



@app.route('/delete/<string:name>', strict_slashes=False)
def delete(name):

	record = check_record(name)

	if isinstance(record, str):
		return record

	db.session.delete(record)
	db.session.commit()
	return redirect('/')



@app.route('/change/<string:name>', strict_slashes=False)
def change(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('change.html', record=record)



@app.route('/records', methods=['POST'], strict_slashes=False)
def add_record():
	
	name = request.form.get('name')
	phone = request.form.get('phone')
	email = request.form.get('email')
	birthday = create_birthday(request.form)
	address = create_address(request.form, ['city', 'street', 'postal_code'])

	if Record.query.filter_by(name=name).first():
		return f'Record {record.id} {record.name} already exists!', 409

	if Phone.query.filter_by(phone=phone).first():
		return f'Phone {phone} already exists!', 409

	if Email.query.filter_by(email=email).first():
		return f'Email {email} already exists!', 409

	record = Record(name=name)
	birthday = Birthday(birthday=birthday)
	address = Address(address=address)

	db.session.add_all([record, birthday, address])
	db.session.commit()

	phone = Phone(phone=phone, record_id=record.id)
	email = Email(email=email, record_id=record.id)
	record_address = Record_Address_Relationship(address_id=address.id, record_id=record.id)
	record.birthday_id = birthday.id

	db.session.add_all([phone, email, record_address])
	db.session.commit()

	return redirect('/')



# -----------------Add record handlers----------------


@app.route('/add_phone/<string:name>', strict_slashes=False)
def add_phone_form(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('add_field.html', record=record, add_type='phone')


@app.route('/add_email/<string:name>', strict_slashes=False)
def add_email_form(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('add_field.html', record=record, add_type='email')


@app.route('/add_birthday/<string:name>', strict_slashes=False)
def add_birthday_form(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('add_field.html', record=record, add_type='birthday')


@app.route('/add_address/<string:name>', strict_slashes=False)
def add_address_form(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('add_field.html', record=record, add_type='address')


# -----------------Change record handlers----------------


@app.route('/ch_name/<string:name>', strict_slashes=False)
def ch_name_form(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('change_field.html', record=record, ch_type='name')


@app.route('/ch_phone/<string:name>', strict_slashes=False)
def ch_phone_form(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('change_field.html', record=record, ch_type='phone')


@app.route('/ch_email/<string:name>', strict_slashes=False)
def ch_email_form(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('change_field.html', record=record, ch_type='email')


@app.route('/ch_birthday/<string:name>', strict_slashes=False)
def ch_birthday_form(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('change_field.html', record=record, ch_type='birthday')


@app.route('/ch_address/<string:name>', strict_slashes=False)
def ch_address_form(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('change_field.html', record=record, ch_type='address')



# -----------------Delete record handlers----------------


@app.route('/del_phone/<string:name>', strict_slashes=False)
def del_phone_form(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('del_field.html', record=record, del_type='phone')


@app.route('/del_email/<string:name>', strict_slashes=False)
def del_email_form(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('del_field.html', record=record, del_type='email')


@app.route('/del_address/<string:name>', strict_slashes=False)
def del_address_form(name):
	record = Record.query.filter_by(name=name).first()
	return render_template('del_field.html', record=record, del_type='address')


# ================Change methods (routes)================


@app.route('/records/<string:name>/name', methods=['POST'], strict_slashes=False)
def change_name(name):

	record = check_record(name)

	if isinstance(record, str):
		return record

	new_name = request.form.get('new_name')
	record.name = new_name
	db.session.commit()
	return redirect('/')



@app.route('/records/<string:name>/add_email', methods=['POST'], strict_slashes=False)
def add_email(name):

	record = check_record(name)

	if isinstance(record, str):
		return record

	email_val = request.form['email']

	if Email.query.filter_by(email=email_val).first():
		return f'Email {email_val} already exists!', 409

	email = check_email(record, email_val)

	if not isinstance(email, str):
		return f'Email {email.email} already exists for record {record.id} {record.name}!'

	email = Email(email=email_val, record_id=record.id)
	db.session.add(email)
	db.session.commit()

	return redirect('/')



@app.route('/records/<string:name>/del_email', methods=['POST'], strict_slashes=False)
def delete_email(name):

	record = check_record(name)

	if isinstance(record, str):
		return record

	email_val = request.form['email']
	email = check_email(record, email_val)

	if isinstance(email, str):
		return email

	db.session.delete(email)
	db.session.commit()

	return redirect('/')



@app.route('/records/<string:name>/ch_email', methods=['POST'], strict_slashes=False)
def change_email(name):

	record = check_record(name)

	if isinstance(record, str):
		return record

	old_email_val = request.form.get('old_email')
	old_email = check_email(record, old_email_val)

	if isinstance(old_email, str):
		return old_email

	new_email_val = request.form.get('new_email')

	if Email.query.filter_by(email=new_email_val).first():
		return f'Email {new_email_val} already exists!', 409

	new_email = check_email(record, new_email_val)

	if not isinstance(new_email, str):
		return f'Email {new_email.email} already exists for record {record.id} {record.name}!'

	db.session.query(Email).filter((Email.record_id == record.id)&(Email.email == old_email_val)).update({'email': new_email_val})
	db.session.commit()

	return redirect('/')



@app.route('/records/<string:name>/add_phone', methods=['POST'], strict_slashes=False)
def add_phone(name):

	record = check_record(name)

	if isinstance(record, str):
		return record

	phone_val = request.form['phone']

	if Phone.query.filter_by(phone=phone_val).first():
		return f'Phone {phone_val} already exists!', 409

	phone = check_phone(record, phone_val)

	if not isinstance(phone, str):
		return f'Phone {phone.phone} already exists for record {record.id} {record.name}!'

	phone = Phone(phone=phone_val, record_id=record.id)
	db.session.add(phone)
	db.session.commit()

	return redirect('/')


@app.route('/records/<string:name>/del_phone', methods=['POST'], strict_slashes=False)
def delete_phone(name):

	record = check_record(name)

	if isinstance(record, str):
		return record

	phone_val = request.form['phone']
	phone = check_phone(record, phone_val)

	if isinstance(phone, str):
		return phone

	db.session.delete(phone)
	db.session.commit()

	return redirect('/')



@app.route('/records/<string:name>/ch_phone', methods=['POST'], strict_slashes=False)
def change_phone(name):

	record = check_record(name)

	if isinstance(record, str):
		return record

	old_phone_val = request.form.get('old_phone')
	old_phone = check_phone(record, old_phone_val)

	if isinstance(old_phone, str):
		return old_phone

	new_phone_val = request.form.get('new_phone')

	if Phone.query.filter_by(phone=new_phone_val).first():
		return f'Phone {new_phone_val} already exists!', 409

	new_phone = check_phone(record, new_phone_val)

	if not isinstance(new_phone, str):
		return f'Phone {new_phone.phone} already exists for record {record.id} {record.name}!'

	db.session.query(Phone).filter((Phone.record_id == record.id)&(Phone.phone == old_phone_val)).update({'phone': new_phone_val})
	db.session.commit()

	return redirect('/')



@app.route('/records/<string:name>/add_address', methods=['POST'], strict_slashes=False)
def add_address(name):

	record = check_record(name)

	if isinstance(record, str):
		return record

	address_val = create_address(request.form, ['city', 'street', 'postal_code'])
	address = check_address(record, address_val)

	if not isinstance(address, str):
		return f'Such address already exist for record {record.id} {record.name}!'

	address = Address(address=address_val)
	db.session.add(address)
	db.session.commit()

	rec_addr = Record_Address_Relationship(address_id=address.id, record_id=record.id)
	db.session.add(rec_addr)
	db.session.commit()

	return redirect('/')

	

@app.route('/records/<string:name>/del_address', methods=['POST'], strict_slashes=False)
def delete_address(name):

	record = check_record(name)

	if isinstance(record, str):
		return record

	address_val = create_address(request.form, ['city', 'street', 'postal_code'])
	address = check_address(record, address_val)

	if isinstance(address, str):
		return address

	db.session.delete(address)
	db.session.commit()

	return redirect('/')



@app.route('/records/<string:name>/ch_address', methods=['POST'], strict_slashes=False)
def change_address(name):

	record = check_record(name)

	if isinstance(record, str):
		return record

	if request.method == 'POST':
		old_address = create_address(request.form, ['old_city', 'old_street', 'old_postal_code'])
		address = check_address(record, old_address)

		if isinstance(address, str):
			return address

		new_address = create_address(request.form, ['new_city', 'new_street', 'new_postal_code'])
		address = check_address(record, new_address)

		if not isinstance(address, str):
			return f'Such address already exist for record {record.id} {record.name}!'

		filter_query = (Address.records.any(id=record.id)) & (Address.address == old_address)
		address = db.session.query(Address).filter(filter_query).first()
		address.address = new_address
		db.session.commit()

		return redirect('/')



@app.route('/records/<string:name>/ch_birthday', methods=['POST', 'DELETE'], strict_slashes=False)
def change_birthday(name):
	
	record = check_record(name)

	if isinstance(record, str):
		return record

	birthday=create_birthday(request.form)
	record.birthday_val = birthday
	db.session.commit()
	return redirect('/')



@app.route('/records/<string:name>/del_birthday', strict_slashes=False)
def delete_birthday(name):
	
	record = check_record(name)

	if isinstance(record, str):
		return record

	birthday = db.session.query(Birthday).filter(Birthday.records.any(id=record.id)).first()

	if birthday:
		db.session.delete(birthday)
		db.session.commit()

	return redirect('/')
