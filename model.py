from database import Base
from sqlalchemy import Column,Integer,String
class User(Base):
    __tablename__ ="data"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(50))
    email = Column(String(100),unique=True)
    password = Column(String(50))
    
    
class Post(Base):
    __tablename__ ="post"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(50))
    content = Column(String(100))