import email
import enum
from database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, Integer, String,ForeignKey

class ClubType(str,enum.Enum):
    public="public"
    private="private"
    one_v_one="1v1"

class Status(str,enum.Enum):
    pending="pending"
    accepted="accepted"
    rejected="rejected"  


class RequestType(str,enum.Enum):
    request="request"
    invite="invite"      

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
    club_type=Column(Enum(ClubType),nullable=False,default=ClubType.public)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()")
    creator_id=Column(Integer,ForeignKey("account.id",ondelete="CASCADE"),nullable=True)

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


class Club_members(Base):
    __tablename__="club_members"
    id=Column(Integer,primary_key=True,nullable=False)
    account_id=Column(Integer,ForeignKey("accounts.id",ondelete="CASCADE"),nullable=False)
    club_id=Column(Integer,ForeignKey("club.id",ondelete="CASCADE"),nullable=False)
    joined_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()")


class Club_Request(Base):
    __tablename__="club_requests"
    id=Column(Integer,primary_key=True,nullable=False)
    account_id=Column(Integer,ForeignKey("accounts.id",ondelete="CASCADE"),nullable=False)
    club_id=Column(Integer,ForeignKey("club.id",ondelete="CASCADE"),nullable=False)
    status=Column(Enum(Status),nullable=False,default=Status.pending)
    request_type=Column(Enum(RequestType),nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()")
