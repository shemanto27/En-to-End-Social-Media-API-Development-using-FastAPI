from fastapi import status, HTTPException, Response, Depends, APIRouter
from .. import models #so that we can perform query using sqlalchemy
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import *
from ..utils import *

router = APIRouter(prefix="/users", tags=["Users"])

# -------------USER Routes

#------CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=userResponseSchema)
async def create_user(user: userSchema, db: Session = Depends(get_db)):
    
    check_user_exist = db.query(models.User).filter(models.User.email == user.email).first()
    if check_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exist")

    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ---------READ
@router.get("/{id}", response_model=userResponseSchema)
async def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User of id {id} does not exists")
    return user

