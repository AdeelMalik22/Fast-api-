from jose import JWTError ,jwt
from datetime import datetime,timedelta,timezone
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import schema
oauth_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_token(data:dict):
    
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=1)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        
        if not id:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
        return token_data
    except JWTError as e:
        print(e)
    

def current_user(token:str = Depends(oauth_schema)):
   
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials", headers={"WWW-Athenticate":"Barear"})
    
    return verify_access_token(token,credentials_exception)