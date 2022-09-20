from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(
        prefix="/vote",
        tags=['Vote']
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db : Session = Depends(get_db), current_user : int = Depends(get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:# there can be other users who liked the post other than current_user
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has already voted on post {vote.post_id}")
        new_data = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_data)
        db.commit()
        return {"message":"successfully added vote"}
    
    else:# if user wants to dislike or delete his vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted/dis-liked vote"}