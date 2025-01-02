from sqlalchemy import Column,Integer, String, Boolean, ForeignKey, DateTime, func
from .database import Base
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String, nullable=False)
    author = Column(String,nullable=False,server_default="Shemanto Sharkar")
    description = Column(String,nullable=False)
    published = Column(Boolean,nullable=False,server_default='TRUE')
    category = Column(String,nullable=True)
    published_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate= func.now())
    user_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship('User') #refering class.this relationship retrive all user data based on user_id


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())


class Vote(Base):
    __tablename__ = "votes"
    blog_id = Column(Integer, ForeignKey(column="blogs.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE"), primary_key=True)
