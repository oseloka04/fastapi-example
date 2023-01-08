from random import randrange
from typing import Optional,List
from pydantic import BaseModel
from fastapi import Depends,Query, FastAPI, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session,query
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from app import oauth2
from .. import models, schemas
from .. datasource import engine, SessionLocal, get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

class post(BaseModel):
    title:str
    content:str
    published: bool = True

while True:

 try:
     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
     password='surgeon',port=5432, cursor_factory=RealDictCursor)
     cursor = conn.cursor()
     print('Database was connected succesfully')
     break
 except Exception as error:
    print('connecting to database failed') 
    print('error', error)
    time.sleep(2)   


#@router.get("/", response_model=list[schemas.Post])
@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    

    posts = db.query(models.post).filter(models.post.title.contains(search)).limit(limit).offset(skip).all()
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    results = db.query(models.post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.post.id, 
    isouter=True).group_by(models.post.id).filter
    (models.post.title.contains(search)).limit(limit).offset(skip).all()

    return results
 

@router.post("/", status_code=status.HTTP_201_CREATED,
 response_model=schemas.Post)
def create_posts(post: post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published)
   #VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    #new_post = cursor.fetchone()

    #conn.commit()
     print(current_user)
     new_post = models.post(owner_id=current_user.id, **post.dict())
     #new_post = models.post(title=post.title, content=post.content, published=post.published)
     db.add(new_post)
     db.commit()
     db.refresh(new_post)
     return new_post
     


@router.get("/{idf}", response_model=List[schemas.Post])
def get_post(idf:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    cursor.execute("""SELECT * from posts WHERE id = %s""", (str(idf),) )
    post = cursor.fetchone()
    print(post)
    post = db.query(models.post).filter(models.post.owner_id == current_user.id).all()
    
    
    if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f"post with id: {idf} was not found")
    return {"post_detail": post}


@router.delete("/{idf}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(idf: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
     #(str(idf),))
    #deleted_post = cursor.fetchone
    #conn.commit()
    post_query = db.query(models.post).filter(models.post.id == idf)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id: {idf} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.
        HTTP_403_FORBIDDEN, detail='not authorised to perform requested action')

    post_query.delete(synchronize_session=False)
    db.commit    

    print(current_user.email)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{idf}")
def update_post(idf: int, post: post,  current_user: int = Depends(oauth2.get_current_user)):
    cursor.execute("""UPDATE posts SET title = %s, content = %s,
     published =%s WHERE id = %s RETURNING  *""",
     (post.title, post.content, post.published, str(idf)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id: {idf} does not exist")
   
    return {"data": updated_post}


