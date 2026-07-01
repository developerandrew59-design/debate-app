from typing import Optional, List
from models import ClubType
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
    club_type: ClubType= ClubType.public

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

class ArgumentreturnwithVotesnoreplies(BaseModel):
    Argument: Argumentreturn
    upvotes: int
    downvotes: int 

    class Config():
        from_attributes= True   

class ArgumentreturnwithVotes(BaseModel):
    Argument: Argumentreturn
    counter_arguments: List[ArgumentreturnwithVotesnoreplies]
    upvotes: int
    downvotes: int  
    class Config():
        from_attributes= True  


class Tokendata(BaseModel):
    id: int


class Token(BaseModel):
    acess_token: str
    token_type: str    


class Vote(BaseModel):
    vote: bool
    argument_id: int

class VoteReturn(Vote):
    id: int
    account_id: int
    created_at: datetime