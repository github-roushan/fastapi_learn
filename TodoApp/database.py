from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import BASE_DIR, POSTGRES_DB, POSTGRES_PASS, POSTGRES_USER


## For Sqlite Database
# SQLALCHEMY_SQLITE_DATABASE_URL = f'sqlite:///{BASE_DIR}/todosapp.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

## For Postgres Database
SQLALCHEMY_PG_DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@localhost/{POSTGRES_DB}'
engine = create_engine(SQLALCHEMY_PG_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

Base = declarative_base()