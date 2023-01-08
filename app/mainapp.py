from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from . import models
from .datasource import engine, get_db
from .router import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
my_posts = [{'title': "title of post 1", "content": "content of post 1", "idf": 1}, {
    "title": "favorite food", "content": "i like pizza", "idf":2}]

def find_post(idf):
    for p in my_posts:
        if p["idf"] == idf:
            return p

def find_index_post(idf):
    for i,p in enumerate(my_posts):
        if p['idf'] == idf:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root ():
    return {"message": "Hello World, welcome to my api"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

   posts = db.query(models.post).all()
   return posts
