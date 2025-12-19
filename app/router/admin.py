


# @router.get("/", response_model=List[schemas.User_show] ,status_code=status.HTTP_200_OK)
# def get_users(db: Session = Depends(get_db)):
#     users=db.query(models.User).all()
#     if not users :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no users found")
#     return users