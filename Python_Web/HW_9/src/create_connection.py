from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+mysqlconnector://root:password@127.0.0.1:3306/hw_9')
session_class = sessionmaker(bind=engine)
session = session_class()

Base = declarative_base()