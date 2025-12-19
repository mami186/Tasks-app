from typing import List
from fastapi import APIRouter  ,Depends ,HTTPException ,status
from .. import database ,models ,schemas
from sqlalchemy.orm import Session
from .. import oauth2
router = APIRouter(
    prefix="/user/tags",
    tags=["tags"]
)

get_db= database.get_db



@router.get("/",response_model=List[schemas.Show_tags],status_code=status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db),current_user:schemas.TokenData =Depends(oauth2.get_current_user)):
    tag=db.query(models.Tag).filter(models.Tag.user_id == current_user.id).all()
    return tag

@router.get(f"/{id}" ,response_model=schemas.Show_tags ,status_code=status.HTTP_200_OK)
def tag_Num(id:int ,db: Session = Depends(get_db) ,current_user:schemas.TokenData =Depends(oauth2.get_current_user)):
    tag= db.query(models.Tag).filter(models.Tag.id == id , models.Tag.user_id == current_user.id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f" no task found with id {id}")
    return tag


@router.post("/",status_code=status.HTTP_201_CREATED)
def create_tag(request:schemas.Tags , db: Session = Depends(get_db),current_user:schemas.TokenData =Depends(oauth2.get_current_user)):
    new_tag= models.Tag(name=request.name ,color=request.color ,user_id =current_user.id)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return  new_tag


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def edit_tags(id:int ,request:schemas.Tags , db: Session = Depends(get_db),current_user:schemas.TokenData =Depends(oauth2.get_current_user)):
    tag = db.query(models.Tag).filter(models.Tag.id ==id  ,models.Tag.user_id == current_user.id)
    if not tag.first() :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    update_data = request.model_dump(exclude_unset=True)

    tag.update(update_data)
    db.commit()
    return {"message": "Task updated successfully"}


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_tags(id:int, db: Session = Depends(get_db),current_user:schemas.TokenData =Depends(oauth2.get_current_user)):
    tag = db.query(models.Tag).filter(models.Tag.id ==id ,models.Tag.user_id == current_user.id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(tag)
    db.commit()
    return {"message":"tag deleted successfully"}


@router.post("/tasks/{task_id}/tags/{tag_id}", status_code=status.HTTP_202_ACCEPTED)
def add_tag_to_task(task_id: int,tag_id: int,db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id,models.Task.user_id == current_user.id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id,models.Tag.user_id == current_user.id).first()

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    if tag in task.tags:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag already assigned to this task"
        )

    task.tags.append(tag)
    db.commit()
    return {"message": "Tag added to task successfully"}


@router.delete("/tasks/{task_id}/tags/{tag_id}", status_code=status.HTTP_200_OK)
def remove_tag_from_task(task_id: int,tag_id: int,db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id,models.Task.user_id == current_user.id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found")

    tag = db.query(models.Tag).filter(models.Tag.id == tag_id,models.Tag.user_id == current_user.id).first()

    if not tag or tag not in task.tags:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not assigned to this task"
        )

    task.tags.remove(tag)
    db.commit()
    return {"message": "Tag removed from task successfully"}
