from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import datasource, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentiction"])

@router.post('/login',)
def login( User_credentials: OAuth2PasswordRequestForm = Depends(), 
db: Session = Depends(datasource.get_db)):

    user = db.query(models.user).filter(models.user.email == User_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail=f"invalid credentials")
     

    if not utils.verify(User_credentials.password, user.password ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"invalid credentails") 

    access_token = oauth2.create_access_token(data = {"user_id": user.id})    

    return {"access_token": access_token, "token_type": "bearer"}
    