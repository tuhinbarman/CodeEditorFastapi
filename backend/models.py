from database import Base
from sqlalchemy import String,Column,Integer,DateTime,Text

class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer,primary_key=True,index=True)
    createdby = Column(String(length=255),nullable=False)
    createddate = Column(DateTime,nullable=False)
    no_of_users_allowed = Column(Integer)
    code = Column(Text)
    last_code_modified_date = Column(DateTime,nullable=True)

    