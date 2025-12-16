from fastapi import APIRouter , Depends ,HTTPException ,status
from .. import database ,models,schemas
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/user",
    tags=["Users"]
)

get_db =database.get_db

@router.post("/")
def create_user(request:schemas.User , db: Session = Depends(get_db)):
    new_user= models.User(name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.get("/user")
def get_users(db: Session = Depends(get_db)):
    users=db.query(models.User).all()
    if not users :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no users found")
    return users

@router.get("/tasks")
def get_tasks(id:int , db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.user_id == id).all()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no tasks found")
    return tasks