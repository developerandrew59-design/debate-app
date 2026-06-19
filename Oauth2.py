from fastapi import Depends, HTTPException, status
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from config import settings
from datetime import timezone,timedelta,datetime
from sqlalchemy.orm import Session
from database import get_db
from schemas import Tokendata
import models

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

def create_acess_token(data:dict):
    encode=data.copy()
    expiry=datetime.now(timezone.utc)+timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp":expiry})
    encoded_data=jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_data

def verify_acess_token(token:str,creds_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str=str(payload.get('user_id'))
        if id is None:
            raise creds_exception
        token_data=Tokendata(id=id)
    except JWTError:
        raise creds_exception

    return token_data  

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
      creds_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="could not validate creditinals",
                                    headers={"WWW-Authenticate":"bearer"})
      token=verify_acess_token(token,creds_exception)

      user=db.query(models.User).filter(models.User.id==token.id).first()

      return user