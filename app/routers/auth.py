from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import utils, oauth2, schemas, models

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    data = db.query(models.User).filter(models.User.email == user.username).first()

    if data == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Wrong credentials, Try again")

    if not utils.verify(user.password, data.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Wrong credentials given, Please try agian")

    access_token = oauth2.create_access_token(data={"user_id": data.id})

    return {"access_token": access_token, "token_type": "bearer"}