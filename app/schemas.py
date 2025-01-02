from pydantic import BaseModel,EmailStr
from sqlmodel import Field
from typing import Optional

# ----------User Schema
class userSchema(BaseModel):
    email: EmailStr
    password: str
    country: str | None = None
    user_name: str | None = None

class userResponseSchema(BaseModel):
    user_name: str | None
    email: EmailStr
    country: str | None
    class Config:
        from_attributes = True


#-------Blog Schema
class blogSchema(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)  #Field is use to add extra constrains
    title: str
    author: str = "Shemanto Sharkar"
    description: str
    published: bool = True
    category: str | None

    

class blogResponseSchema(BaseModel):
    title: str
    description: str
    published: bool
    category: str
    owner: userResponseSchema
    class Config:
        from_attributes = True



#-----------Authentication Schema
class authSchema(BaseModel):
    email: EmailStr
    password: str

class tokenSchema(BaseModel):
    access_token: str
    token_type: str
    class Config:
        from_attributes = True

class tokenDataSchema(BaseModel):
    id: str | None



#--------------Vote Schema
class voteSchema(BaseModel):
    blog_id: int
    dir: int = Field(..., ge=0, le=1) #ellipsis(...) indicates that this field is required