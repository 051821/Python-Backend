#6

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from .. import model, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, get_db


router = APIRouter(
    tags=['Users']
)

@router.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user_dict = user.dict()
    user_dict["password"] = utils.hash(user.password)

    new_user = model.User(**user_dict)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/user/{id}',response_model=schemas.UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail = "USer not found")
    
    return user

    

