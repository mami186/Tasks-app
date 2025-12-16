from typing import Optional ,List
from pydantic import BaseModel


class Task(BaseModel):
    name:Optional[str]=None
    body:str

class Tag(BaseModel):
    tag:str

class Show_task(Task):
    user_id:int
    complete:bool
    pin :bool

class User(BaseModel):
    name: str
    email: str
    password: str

class TaskId(BaseModel):
    id:int