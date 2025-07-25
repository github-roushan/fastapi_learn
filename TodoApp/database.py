from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import pathlib
BASE_DIR = pathlib.Path(__file__).parent
SQLALCHEMY_DATABASE_URL = f'sqlite:///{BASE_DIR}/todos.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

Base = declarative_base()