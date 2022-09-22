from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from ..oauth2 import get_current_user
from sqlalchemy import func

router = APIRouter(
        prefix='/posts',
        tags=['Posts']
         )# we add tags for /docs link repr segregating posts, users sections


@router.get('/', response_model=List[schemas.PostOut])
def get_post_updates(db: Session = Depends(get_db), current_user : dict = Depends(get_current_user), 
                     limit:int = 10, skip:int = 0, search:Optional[str] = ""):
    
    data = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("no_of_votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id
        ).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        # .join() is by default left innner join and to set it outer, we pass in paramenters
    return results

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createPost(msg:schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):# adds data to different id
    data = models.Post(owner_id=current_user.id, **msg.dict())
    db.add(data)
    db.commit()
    db.refresh(data)# similar to RETURNING *
    return data

@router.get("/latest", response_model=schemas.PostResponse)
def post_latest(db: Session = Depends(get_db), current_user : dict = get_current_user):
    data = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return data

@router.get('/{id}', response_model=schemas.PostOut)
def retrieve_posts(id : int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    data = db.query(models.Post, func.count(models.Vote.post_id).label("no_of_votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id
        ).filter(models.Post.id == id).first()
        
    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with {id} does not exist')
    
    # if data.owner_id!=current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform request at action")
    
    return data    

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    data = db.query(models.Post).filter(models.Post.id == id)
    
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with {id} does not exist')
    
    if data.first().owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform request at action")
    
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)# for raise to func and display in postman we should use Response()

@router.put('/{id}', response_model=schemas.PostResponse)# update func
def update_posts(id:int, post:schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):# adds new data to the same id as prev whereas post adds data to different id
    new_data = db.query(models.Post).filter(models.Post.id == id)
    first_row = new_data.first()
    if first_row == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The row-{id} is not there in table")
    
    if first_row.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform request at action")
    
    new_data.update(post.dict(), synchronize_session=False)
    db.commit()
    # db.refresh(new_data)    
    return new_data.first()
