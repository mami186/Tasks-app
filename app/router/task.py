from fastapi import APIRouter  ,Depends ,HTTPException ,status
from .. import database ,models ,schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/task",
    tags=["Tasks"]
)

get_db= database.get_db



@router.get("/{id}" ,response_model=schemas.Show_task)
def task_No(id:int ,db: Session = Depends(get_db)):
    task= db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f" no task found with id {id}")
    return task

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    tasks=db.query(models.Task).all()
    if not tasks :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no tasks found")
    return tasks

@router.post("/")
def create_task(request:schemas.Task , db: Session = Depends(get_db)):
    new_task= models.Task(name=request.name ,body=request.body ,user_id =1)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.put("/{id}")
def edit(id:int ,request:schemas.Task , db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id ==id)
    if not task.first() :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    update_data = request.model_dump(exclude_unset=True)

    task.update(update_data)
    db.commit()
    return {"message": "Task updated successfully"}


@router.delete("/{id}")
def delete(id:int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id ==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

