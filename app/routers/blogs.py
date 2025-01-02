from fastapi import status, HTTPException, Response, Depends, APIRouter
from .. import models #so that we can perform query using sqlalchemy
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import *
from ..oauth2 import *
from typing import Optional


router = APIRouter(prefix="/blogs", tags=["Blogs"])

# --------------------Blogs Routes

# -------CREATE
@router.post("/",status_code=status.HTTP_201_CREATED, response_model= blogResponseSchema)
async def create_blog(blog : blogSchema, db : Session = Depends(get_db), current_user: int = Depends(get_current_active_user)):
    
    new_blog = models.Blog(user_id=current_user.id, **blog.dict()) #creating new blog post record,converting the pydantic model to dict and then unpacking the dict so that we dont have to write all the columns
    
    db.add(new_blog) # adding it to out db 
    db.commit() #commit changes
    db.refresh(new_blog) #reload that newly created record in new_blog variable
    return new_blog



# ---------READ
@router.get("/", response_model= list[blogResponseSchema])
async def get_blogs(db: Session = Depends(get_db), limit:int = 10, skip:int = 0, search: Optional[str] = ""):
    
    all_blogs = db.query(models.Blog).filter(models.Blog.title.contains(search)).limit(limit).offset(skip).all()
    return all_blogs

@router.get("/{id}", response_model= blogResponseSchema)
async def get_blog_by_id(id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id: {id}, does not exist")
    return blog





# ---------DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_active_user)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)

    blog = blog_query.first()

    if blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if blog.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    blog_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)





# --------UPDATE
@router.put("/{id}", response_model= blogResponseSchema)
async def update_blog(id:int, blog:blogSchema, db: Session = Depends(get_db), current_user: int = Depends(get_current_active_user)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    old_blog = blog_query.first()

    if old_blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"This id:{id} does not exist")

    if old_blog.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Perform this Task")
        
    blog_query.update(blog.dict(), synchronize_session=False) #must pass a python dict
    db.commit()
    return blog_query.first()





