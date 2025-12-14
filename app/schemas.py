from typing import Optional, List
from pydantic import BaseModel


class Task(BaseModel):
    name:Optional[str]=None
    body:str
    user_id:int

class Tag(BaseModel):
    tag:str

class Show_task(Task):
    completed:bool
    tag:List[Tag]=[]

class User(BaseModel):
    name: str
    email: str
    password: str

class TaskId(BaseModel):
    id: int