import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Set up the SQLAlchemy engine and model
engine = create_engine("mysql://user:password@host:port/database")
Base = declarative_base()

class MyModel(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True)
    data = Column(String)

# Read data from the API
response = requests.get("http://api.example.com/data")
data = response.json()

# Store the data in the database
Session = sessionmaker(bind=engine)
session = Session()

record = MyModel(data=data)
session.add(record)
session.commit()
