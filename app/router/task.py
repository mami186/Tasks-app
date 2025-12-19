from typing import List
from fastapi import APIRouter  ,Depends ,HTTPException ,status
from .. import database ,models ,schemas
from sqlalchemy.orm import Session
from .. import oauth2
router = APIRouter(
    prefix="/task",
    tags=["Tasks"]
)

get_db= database.get_db



@router.get("/",response_model=List[schemas.Show_task],status_code=status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db),current_user:schemas.TokenData =Depends(oauth2.get_current_user)):
    tasks=db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
    return tasks


@router.get("/{id}" ,response_model=schemas.Show_task ,status_code=status.HTTP_200_OK)
def task_No(id:int ,db: Session = Depends(get_db) ,current_user:schemas.TokenData =Depends(oauth2.get_current_user)):
    task= db.query(models.Task).filter(models.Task.id == id , models.Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f" no task found with id {id}")
    return task


@router.post("/",status_code=status.HTTP_201_CREATED)
def create_task(request:schemas.Task , db: Session = Depends(get_db),current_user:schemas.TokenData =Depends(oauth2.get_current_user)):
    new_task= models.Task(name=request.name ,body=request.body ,user_id =current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return  new_task


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def edit(id:int ,request:schemas.Task , db: Session = Depends(get_db),current_user:schemas.TokenData =Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id ==id  ,models.Task.user_id == current_user.id)
    if not task.first() :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    update_data = request.model_dump(exclude_unset=True)

    task.update(update_data)
    db.commit()
    return {"message": "Task updated successfully"}


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, db: Session = Depends(get_db),current_user:schemas.TokenData =Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id ==id ,models.Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task)
    db.commit()
    return 
