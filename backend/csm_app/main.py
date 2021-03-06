from fastapi import FastAPI, Depends, HTTPException
from csm_app import crud, models, schemas
from csm_app.database import SessionLocal, engine
from typing import List
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
CSM_Backend = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@CSM_Backend.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.user_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered!")
    return crud.create_user(db=db, user=user)


@CSM_Backend.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@CSM_Backend.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@CSM_Backend.get("/")
async def root():
    return {"message": "This is the root of the API. Please go to site.com/docs to see the documentation"}

# Insert into the DB with something like INSERT INTO users VALUES(1, 'petersteele111@gmail.com', 'Peter', 'Steele', 'petersteele111', '012sdf02501sdf40sdf', 'True', 'True', 'Software Developer', 'Software Developer with 10 Years experience', 'Williamsburg, Michigan', '2020-03-22 12:00:00');