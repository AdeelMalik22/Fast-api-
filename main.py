from fastapi import FastAPI,Depends ,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import engine,SessionLocal,Base
from sqlalchemy.orm import Session
import model
import utilis,Auth


from model import User ,Post
from schema import *
import utilis



Base.metadata.create_all(bind=engine)
app = FastAPI()



def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()
        
        
#-------------------------------------login User ----------------------------------------------
        
@app.post("/login")
def create_user(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(model.User).filter(User.email==user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=403,detail="Invalid Credentials")
    
    if not utilis.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=403,detail="invalid Credentials")
    
    
    token = Auth.create_token(data={"user_id":user.id,"Email":user.email})
    return {"Access Token":token ,"Token type":"Jwt token"}




@app.get("/PATH",response_model=list[GetUserSchema])
def index(db:Session=Depends(get_db)):
    return db.query(User).all()
    

@app.post("/PATH",response_model=UserSchema) 
def put_user(user:UserSchema,db:Session=Depends(get_db)):
    hassed_passed = utilis.hash(user.password)
    user.password = hassed_passed
    u = User(name=user.name,email=user.email,password=user.password)
    db.add(u)
    db.commit()
    return u

@app.put("/PATH/{user_id}",response_model=UpdateSchema) 
def update_user(user_id:int,user:UpdateSchema,db:Session=Depends(get_db)):
    
    u = db.query(User).filter(User.id==user_id).first()
    if not u:
        raise HTTPException(status_code=404,detail=f"User with id {user_id} doesnot exists")
    u.email= user.email
    u.password=user.password
    db.add(u)
    db.commit()
    return u



   
    
@app.delete("/PATH/{user_id}")
def delete_user(user_id:int,db:Session=Depends(get_db)):
    
    try:
        u = db.query(User).filter(User.id==user_id).first()
        db.delete(u)
        db.commit()
        return {f"User of id {user_id} has been deleted"}
    except:
        raise HTTPException(status_code=404,detail="User not found......")
    finally:
        db.close()
        
        
        
#--------------------------Post data ----------------------------------------

@app.get("/post",response_model=list[GetPOst])
def index(db:Session=Depends(get_db),get_current_user:Session = Depends(Auth.current_user)):
    return db.query(Post).all()
    


@app.post("/post",response_model=CreatePost,) 
def create_post(post:CreatePost,db:Session=Depends(get_db), get_current_user:int = Depends(Auth.current_user)):
    u = Post(title=post.title,content=post.content)
    db.add(u)
    db.commit()
    return u

        

   


