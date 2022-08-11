from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_string = "postgresql+psycopg2://user_bd:pwd_bd@localhost:5432/name_bd"
engine = create_engine(db_string)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()