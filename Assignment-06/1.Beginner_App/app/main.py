from sqlalchemy import create_engine,Column,Integer,NVARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from fastapi import FastAPI,HTTPException,Depends


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
con=engine.connect()


Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id=Column(Integer,primary_key=True)
    name=Column(NVARCHAR(20))
    email=Column(NVARCHAR(30))

Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    db=SessionLocal()
    yield db
    db.close()


@app.get("/users")
def read_user(user_id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="user not found")
    return user

@app.post("/users")
def create_user(name:str,email:str,db:Session=Depends(get_db)):
    user=User(name=name,email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}")
def remove_user(user_id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="user not found")
    db.delete(user)
    db.commit()
    return{"message":"user deleted successfully"}  

@app.put("/users/{user_id}")
def create_user(user_id:int,name1:str,email1:str,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id== user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="user not found")
    user.name = name1
    user.email = email1
    db.commit()
    db.refresh(user)
    return user