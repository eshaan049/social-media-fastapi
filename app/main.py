from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)# this checks whether a table in DB already exists else action to be done

app = FastAPI()

origins = ["https://www.google.com"]# if all things should access then origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origin=origins,
    allow_credentials=True,
    allow_methods=["*"],# we can allow certain HTTP methods too
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
async def root():# in flask we use route func both are same tho
    return {"message": "Hello Amma"}