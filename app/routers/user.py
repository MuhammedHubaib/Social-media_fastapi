from .. import schema,models,utilit
from fastapi import FastAPI,HTTPException,status,Response,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/user',
                   tags=['user'])

@router.get("/",response_model=list[schema.UserOut])
def all_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def create_user(user: schema.UserCreate,db: Session = Depends(get_db)):
    
    hashed_password = utilit.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
@router.get("/{id}",response_model=schema.UserOut)
def gett_user(id:int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The user with ID {id} id not found")
    
    return user