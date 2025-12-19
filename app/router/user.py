from fastapi import APIRouter , Depends ,HTTPException ,status
from .. import database ,models,schemas
from sqlalchemy.orm import Session
from typing import List
from .. import hash
from .. import oauth2



router=APIRouter(
    prefix="/user",
    tags=["Users"]
)

get_db =database.get_db

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_user(request:schemas.User , db: Session = Depends(get_db)):
    hashed = hash.hash_password(request.password)
    new_user= models.User(name=request.name, email=request.email, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email, "name": new_user.name}


@router.delete("/me",status_code=status.HTTP_204_NO_CONTENT)
def delete_user( db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this user"
        )
    db.delete(user)
    db.commit()
    return {"message": "Your account has been deleted successfully"}

@router.put("/me",status_code=status.HTTP_202_ACCEPTED)
def update_user(request:schemas.User_update,db:Session=Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this user"
        )

    updated = request.model_dump(exclude_unset=True)
    user.update(updated)

    db.commit()
    return {"message": "Task updated successfully"}


@router.get("/", response_model=List[schemas.User_show] ,status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users=db.query(models.User).all()
    if not users :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no users found")
    return users



