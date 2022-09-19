from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app():

	app = Flask(__name__, instance_relative_config=True, template_folder='../templates')
	app.config.from_object('config.Config')
	
	db.init_app(app)
	migrate.init_app(app, db)

	with app.app_context():
		from .routes import routes_fintech, routes_currency
		from . import db_models
		db.create_all()

	return app