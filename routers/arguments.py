from ast import mod
from typing import List
from fastapi import APIRouter,Depends, HTTPException,status,Response
from sqlalchemy.orm import Session
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
    argument=models.Argument(**arg.model_dump())
    db.add(argument)
    db.commit()
    db.refresh(argument)

    return argument

@router.get("/",response_model=List[schemas.Argumentreturn])
def get_all_arguments(db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    arguments=db.query(models.Argument).all()

    return arguments

@router.get("/{id}",response_model=schemas.Argumentreturn)
def get_one_argument(id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    argument=db.query(models.Argument).filter(models.Argument.id==id).first()

    if not argument:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"argument with id {id} not found")

    return argument

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

