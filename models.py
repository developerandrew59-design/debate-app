import email

from database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String,ForeignKey

class User(Base):
    __tablename__="accounts"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()")

class Debate(Base):
    __tablename__="club"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()")

class Argument(Base):
    __tablename__="arguments"
    id=Column(Integer,primary_key=True,nullable=False)
    argument=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()") 
    club_id=Column(Integer,ForeignKey("club.id",ondelete="CASCADE"),nullable=False)
    account_id=Column(Integer,ForeignKey("accounts.id",ondelete="CASCADE"),nullable=True)
    parent_id=Column(Integer,ForeignKey("arguments.id",ondelete="CASCADE"),nullable=True)
                
