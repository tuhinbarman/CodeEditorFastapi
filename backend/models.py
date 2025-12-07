from database import Base
from sqlalchemy import (
    String,Column,Integer,DateTime,Text,Float,ForeignKey)
from sqlalchemy.orm import relationship

class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer,primary_key=True,index=True)
    createdby = Column(String(length=255),nullable=False)
    createddate = Column(DateTime,nullable=False)
    no_of_users_allowed = Column(Integer)
    code = Column(Text)
    last_code_modified_date = Column(DateTime,nullable=True)
    language_id = Column(Integer,ForeignKey('code_language.language_id'),nullable=True)

    language = relationship("CodeLanguage",back_populates="rooms")

class CodeLanguage(Base):

    __tablename__ = "code_language"

    language_id = Column(Integer,primary_key=True,index=True)
    language_name = Column(String,nullable=False)
    temp_code = Column(Text)
    version = Column(Float)

    rooms = relationship("Rooms",back_populates="language")



    