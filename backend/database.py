from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from conf import *

engine = create_engine(DATABASE_URL,echo=True)

sessionlocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    except:
        print('Error connecting to db')
    finally:
        db.close()