from fastapi import Depends,HTTPException,status,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..import database
from .. import utilit,schema,models,oauth
from sqlalchemy.orm import Session


router = APIRouter(tags=['authentication'])

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
   
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    
    if not utilit.verify(user_credentials.password,user.password):
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    
    access_token = oauth.creating_token(data= {"user_id": user.id})
    return { "access_token":access_token,"token_type":"bearer"}