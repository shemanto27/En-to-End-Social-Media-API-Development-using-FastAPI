import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from .schemas import *
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .database import *
from sqlalchemy.orm import Session
from . import models
from .config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")  #login endpoint

#SECRET KEY
#ALGORITHM
#EXPIRATION TIME

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):  #data is the payload we want give
    to_encode = data.copy() #making copy of the data,so that original data dont get change
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire}) # adding expire time info in the dictionary
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def varify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # extraction all 3 token data in payload

        id : str = str(payload.get("user_id"))  #to extract specific part

        if id == None:
            raise credential_exception
        token_data = tokenDataSchema(id = id)
    except InvalidTokenError:
        raise credential_exception

    return token_data


def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = varify_access_token(token, credential_exception)

    user = db.query(models.User).filter(token.id == models.User.id).first()

    return user