from typing import Optional

from pydantic import BaseModel,EmailStr
from datetime import datetime


class Userbase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(Userbase):
    pass

class UserReturn(UserCreate):
    id:int
    created_at: datetime

class Clubcreate(BaseModel):
    name: str

class Clubreturn(Clubcreate):
    id:int
    created_at: datetime   

class Argumentcreate(BaseModel):
    argument:str
    club_id:int
    parent_id: Optional[int]=None         

class Argumentreturn(Argumentcreate):
    id: int
    created_at:datetime
    account_id: int


class Tokendata(BaseModel):
    id: int


class Token(BaseModel):
    acess_token: str
    token_type: str    