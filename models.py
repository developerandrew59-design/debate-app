import email
import enum
from database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, Integer, String,ForeignKey

class ClubType(str,enum.Enum):
    public="public"
    private="private"
    one_v_one="1v1"

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
    club_type=Column(Enum(ClubType),nullable=False,default=ClubType.private)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()")

class Argument(Base):
    __tablename__="arguments"
    id=Column(Integer,primary_key=True,nullable=False)
    argument=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()") 
    club_id=Column(Integer,ForeignKey("club.id",ondelete="CASCADE"),nullable=False)
    account_id=Column(Integer,ForeignKey("accounts.id",ondelete="CASCADE"),nullable=False)
    parent_id=Column(Integer,ForeignKey("arguments.id",ondelete="CASCADE"),nullable=True)


class Vote(Base):
    __tablename__="votes"
    id=Column(Integer,primary_key=True,nullable=False)
    vote=Column(Boolean,nullable=False)
    account_id=Column(Integer,ForeignKey("accounts.id",ondelete="CASCADE"),nullable=False)
    argument_id=Column(Integer,ForeignKey("arguments.id",ondelete="CASCADE"),nullable=False) 
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()")

