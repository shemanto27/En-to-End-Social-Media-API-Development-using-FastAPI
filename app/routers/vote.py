from fastapi import status, HTTPException, Response, Depends, APIRouter
from .. import models #so that we can perform query using sqlalchemy
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import *
from ..oauth2 import *


router = APIRouter(
    prefix="/vote",
    tags=["votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_vote(vote: voteSchema, db: Session=Depends(get_db), current_user: int = Depends(get_current_active_user)):

    vote_query =  db.query(models.Vote).filter(models.Vote.blog_id == vote.blog_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{current_user.id} has already voted on {vote.blog_id}")
        else:
            new_vote = models.Vote(blog_id = vote.blog_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return {"msg": "Successfully Added Vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote Does Not Exist!")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"msg": "Successfully Deleted Vote!"}