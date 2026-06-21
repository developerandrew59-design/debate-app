from ast import mod
from typing import List
from fastapi import APIRouter,Depends, HTTPException,status
from sqlalchemy.orm import Session
import Oauth2
import models
from utils import hash
from database import get_db
import schemas

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/",response_model=schemas.UserReturn,status_code=status.HTTP_201_CREATED)
def create_User(user:schemas.UserCreate,db:Session=Depends(get_db)):
    hashed_password=hash(user.password)
    user.password=hashed_password
    user_dict=models.User(**user.model_dump())
    db.add(user_dict)
    db.commit()
    db.refresh(user_dict)

    return user_dict

@router.get("/",response_model=List[schemas.UserReturn])
def get_all_users(lim:int=10,skip:int=0,search:str="",db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    users=db.query(models.User).filter(
        models.User.email.contains(search)
    ).limit(lim).offset(skip).all()

    return users

@router.get("/{id}",response_model=schemas.UserReturn)
def get_one_user(id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    user=db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"account with id {id} not found")

    return user
