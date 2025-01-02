from fastapi import status, HTTPException, Response, Depends, APIRouter
from .. import models #so that we can perform query using sqlalchemy
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import *
from ..utils import verify_user
from ..oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

# --------------------Authentication Routes
@router.post("/login", response_model=tokenSchema)
async def login(user_credential:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #it will give username, password but we need email,not username
    
    #authenticate user
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not Found, check email address is correct or Signup")

    
    if not verify_user(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Password")
    
    #create token
    access_token = create_access_token(data= {"user_id" : user.id}) #whatever payload we want to give

    return {"access_token" : access_token, "token_type" : "bearer"} 