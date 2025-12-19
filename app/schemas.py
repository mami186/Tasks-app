from typing import Optional 
from pydantic import BaseModel


class Task(BaseModel):
    name:Optional[str]=None
    body:str

class Tag(BaseModel):
    tag:str

class Show_task(Task):
    id:int
    user_id:int
    complete:bool
    pin :bool


class User(BaseModel):
    name: str
    email: str
    password: str

    
class User_show(BaseModel):
    id :int
    name:str
    email:str

class User_update(BaseModel):
    name:str
    
class auth(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    id: int
