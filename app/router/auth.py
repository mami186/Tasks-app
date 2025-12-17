from fastapi import APIRouter , Depends , HTTPException , status
from .. import database , models , schemas
from sqlalchemy.orm import Session
from .. import hash

router= APIRouter(
    prefix="/login",
    tags=["Authentication"]
)
@router.post("/",response_model=schemas.User_show,status_code=status.HTTP_200_OK)
def authenticate_user(request:schemas.auth ,db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    if not hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    return user