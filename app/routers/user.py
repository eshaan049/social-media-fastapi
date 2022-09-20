from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
            prefix='/users',
            tags=['users']
         )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user_data = models.User(**user.dict())
    db.add(new_user_data)
    db.commit()
    db.refresh(new_user_data)
    
    return new_user_data

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id : int, db : Session = Depends(get_db)):
    data = db.query(models.User).filter(models.User.id == id).first()
    
    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with {id} does not exist')
    
    return data