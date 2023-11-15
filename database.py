from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db' # <--this was for SQLite
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:571632@localhost/TodoApplicationDatabase'
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:571632@127.0.0.1:3306/TodoApplicationDatabase'

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) <-- this was for SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
