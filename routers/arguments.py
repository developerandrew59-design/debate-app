from ast import mod
from tkinter import TRUE
from typing import List
from fastapi import APIRouter,Depends, HTTPException,status,Response
from sqlalchemy.orm import Session
from sqlalchemy import func,case, label
import models
from database import get_db
import schemas
import Oauth2

router=APIRouter(
    prefix="/arguments",
    tags=['Arguments']
)

@router.post("/",response_model=schemas.Argumentreturn,status_code=status.HTTP_201_CREATED)
def create_argument(arg:schemas.Argumentcreate,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    argument=models.Argument(account_id=current_user.id,**arg.model_dump())
    db.add(argument)
    db.commit()
    db.refresh(argument)

    return argument

@router.get("/",response_model=List[schemas.Argumentreturn])
def get_all_arguments(club_id:int,lim:int=10,skip:int=0,search:str="",db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    arguments=db.query(models.Argument).filter(models.Argument.club_id==club_id,
                                               models.Argument.argument.contains(search)).limit(lim).offset(skip).all()
    return arguments

@router.get("/{id}",response_model=schemas.ArgumentreturnwithVotes)
def get_one_argument(id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    argument=db.query(models.Argument,
                      func.sum(case((models.Vote.vote==True,1),else_=0)).label("upvotes"),
                      func.sum(case((models.Vote.vote==False,1),else_=0)).label("downvotes")).join(models.Vote,models.Argument.id==models.Vote.argument_id,isouter=True).group_by(models.Argument.id).filter(models.Argument.id==id).first()
    

    if not argument:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"argument with id {id} not found")
    

    app_obj, up, down = argument
    
    return {"Argument": app_obj, "upvotes": up, "downvotes": down}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_argument(id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    argument_query=db.query(models.Argument).filter(models.Argument.id==id)
    argument=argument_query.first()

    if not argument:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"argument with id {id} not found")
    
    argument_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

