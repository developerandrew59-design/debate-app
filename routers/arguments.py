from ast import mod
from typing import List
from fastapi import APIRouter,Depends, HTTPException,status
from sqlalchemy.orm import Session
import models
from database import get_db
import schemas

router=APIRouter(
    prefix="/arguments",
    tags=['Arguments']
)

@router.post("/",response_model=schemas.Argumentreturn,status_code=status.HTTP_201_CREATED)
def create_argument(arg:schemas.Argumentcreate,db:Session=Depends(get_db)):
    argument=models.Argument(**arg.model_dump())
    db.add(argument)
    db.commit()
    db.refresh(argument)

    return argument

@router.get("/",response_model=List[schemas.Argumentreturn])
def get_all_arguments(db:Session=Depends(get_db)):
    arguments=db.query(models.Argument).all()

    return arguments

@router.get("/{id}",response_model=schemas.Argumentreturn)
def get_one_argument(id:int,db:Session=Depends(get_db)):
    argument=db.query(models.Argument).filter(models.Argument.id==id).first()

    if not argument:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"argument with id {id} not found")

    return argument