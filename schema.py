from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class CreatePost(BaseModel):
    title:str
    content:str
    
class GetPOst(BaseModel):
    id:int
    title:str
    content:str
    
    class config:
        orm_mode = True








class UserSchema(BaseModel):
    name:str
    email:EmailStr
    password:str  
    
    class config:
        orm_mode=True
      
class GetUserSchema(BaseModel):
    id:int
    name:str
    email:str
    
class UpdateSchema(BaseModel):
    email:EmailStr
    password:str
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional[str]=None
    created_at :datetime
    
    
    
    class config:
        orm_mode=True    