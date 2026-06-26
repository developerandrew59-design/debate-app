from ast import mod
from typing import List
from fastapi import APIRouter,Depends, HTTPException,status,Response
from sqlalchemy.orm import Session
import models
from database import get_db
import schemas
import Oauth2

router=APIRouter(
    prefix="/votes",
    tags=['Vote']
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,response:Response,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    argument=db.query(models.Argument).filter(models.Argument.id==vote.argument_id).first()

    if not argument:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {vote.argument_id} not found")
    
    if argument.account_id==current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= "You cannot vote on your own argument")
    

    vote_query=db.query(models.Vote).filter(models.Vote.argument_id==vote.argument_id,
                                            models.Vote.account_id==current_user.id)
    final_vote=vote_query.first()

    if not final_vote:
        new_vote=models.Vote(account_id=current_user.id,**vote.model_dump())
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)

        response.status_code=status.HTTP_201_CREATED
        return new_vote
    else:
       if final_vote.vote==vote.vote:
           vote_query.delete(synchronize_session=False)

           db.commit()

           response.status_code=status.HTTP_200_OK

           return {"message": "removed a vote(upvote/downvote)"}
       
       if final_vote.vote!=vote.vote:
           vote_query.update({'vote':vote.vote},
                             synchronize_session=False)
           db.commit()

           response.status_code=status.HTTP_200_OK

           return {"message": "toggled it up to the opposite vote case"}



    
