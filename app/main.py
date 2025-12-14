from fastapi import FastAPI
from .router import task , user
from . import database , models , schemas


app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(task.router)
app.include_router(user.router)

