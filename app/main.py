from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import blogs, users, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine) #to create all table in db


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blogs.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

# @app.get("/")
# async def root():
#     return {"msg" : "Hello World!"}