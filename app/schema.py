from pydantic import BaseModel,EmailStr
from typing import Optional

class UserOut(BaseModel):
     
     id : int
     email : EmailStr
     
     class Config:
         from_attributes = True
         
class BasePost(BaseModel):
    title : str
    content : str
    published : bool = True
    owner : UserOut


class CreatePost(BasePost):
    pass

class Post(BasePost):
    id : int
    owner_id : int
    
    class Config:
        from_attributes = True
        
class VoteCount(BaseModel):
    post: Post
    vote_count: int
    
    class Config:
        from_attributes = True

class voteOut(BasePost):
    post: Post
    vote : int
    
    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    
    email : EmailStr
    password : str
         
class UserLogin(BaseModel):
    
    email : EmailStr
    password : str

class VerifyToken(BaseModel):
    
    access_token : str
    token_type: str
    
class TokenData(BaseModel):
    
    id: Optional[int] = None
    
class vote(BaseModel):
    
    posts_id: int
    dir: bool
    