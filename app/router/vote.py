from fastapi import Depends, FastAPI, HTTPException, Response, status, APIRouter
from .. import schemas, datasource, models, oauth2
from sqlalchemy.orm import Session,query

router = APIRouter(prefix="/vote",
tags=["vote"])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session = Depends(datasource.get_db), 
current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.post).filter(models.post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == 
        current_user.id)
    found_vote = vote_query.first()  
    if  (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
             detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id) 
        db.add(new_vote)
        db.commit()
        return {"messege": "sucessfully added vote"} 
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"vote does not exit")

        vote_query.delete(synchronize_session=False)
        db.commit()  

        return {"messesge": "sucessfully deleted vote"}         
        