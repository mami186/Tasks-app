from fastapi import FastAPI
from .router import task , user ,auth ,tags
from . import database , models 


app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)




app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(tags.router)


