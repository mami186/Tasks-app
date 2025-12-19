from typing import Optional ,List
from pydantic import BaseModel


class Task(BaseModel):
    name:Optional[str]=None
    body:str

class Show_tags(BaseModel):
    id:int
    name:str
    color:str

class Show_task(Task):
    id:int
    user_id:int
    complete:bool
    pin :bool
    tags:List[Show_tags]


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

class Tags(BaseModel):
    name:str
    color:Optional[str] = None

class task_pin(BaseModel):
    pin:bool

class task_status(BaseModel):
    complete:bool

class auth(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    id: int

