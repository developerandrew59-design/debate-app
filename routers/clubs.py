from ast import mod
from typing import List, Optional
from fastapi import APIRouter,Depends, HTTPException,status
from sqlalchemy.orm import Session
import models
from database import get_db
import schemas
import Oauth2
from sqlalchemy import or_,exists

router=APIRouter(
    prefix="/clubs",
    tags=['Clubs']
)

@router.post("/",response_model=schemas.Clubreturn,status_code=status.HTTP_201_CREATED)
def create_club(club:schemas.Clubcreate,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    club_dict=models.Debate(**club.model_dump())
    db.add(club_dict)
    db.commit()
    db.refresh(club_dict)

    if not club.club_type == models.ClubType.public:
        club_rows=models.Club_members(account_id=current_user.id,club_id=club_dict.id)
        db.add(club_rows)
        db.commit()
        db.refresh(club_rows)

    return club_dict

@router.get("/",response_model=List[schemas.Clubreturn])
def get_all_clubs(lim:int=100,skip:int=0,search:str="",club_type: Optional[models.ClubType] = None,
                  db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    
    clubs=db.query(models.Debate).filter(
        models.Debate.name.contains(search),
        models.Debate.club_type==club_type,
        or_(
            models.Debate.club_type==models.ClubType.public,
            exists().where(
                models.Club_members.club_id==models.Debate.id,
                models.Club_members.account_id==current_user.id
            )
        )
    ).limit(lim).offset(skip).all()

    return clubs

@router.get("/{id}",response_model=schemas.Clubreturn)
def get_one_club(id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    club=db.query(models.Debate).filter(models.Debate.id==id).first()

    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"club with id {id} not found")
    
    return club

