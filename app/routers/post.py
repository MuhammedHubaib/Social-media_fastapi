from ..database import get_db
from fastapi import HTTPException,status,Response,Depends,APIRouter
from fastapi.encoders import jsonable_encoder
from .. import schema,models,oauth
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional


router = APIRouter(prefix='/posts',tags=['posts'])

@router.get("/")
def hai(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user),
        limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    vote_count = db.query(models.Post,func.count(models.Vote.post_id)).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    
    serialized_vote_count = []
    for post, count in vote_count:
        serialized_post = jsonable_encoder(post)
        serialized_vote_count.append({"post": serialized_post, "vote_count": count})

    return serialized_vote_count


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def new(post : schema.CreatePost,db: Session = Depends(get_db),current_user:int = Depends(oauth.get_current_user)):
    #cursor.execute(""" INSERT INTO posts (name, content, published_on) VALUES (%s,%s,%s) RETURNING* """,
    #               (post.title, post.content, post.published))
    #post = cursor.fetchall
    
    #conn.commit()
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 


@router.get("/{id}",response_model=schema.Post)
def get_post(id: int,response: Response,db: Session = Depends(get_db),
             current_user:int = Depends(oauth.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts WHERE id=(%s)""",(str(id),))
    #post = cursor.fetchone
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message":f"The post with ID{id} is not found"})
        
    print(post)
    
    
    return post


@router.delete("/{id}",response_model=schema.Post)
def delete_post(id:int, db: Session = Depends(get_db),current_user:int = Depends(oauth.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING* """,(str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail={"message":f"The post with ID {id} is not found"})
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you are not autherised to perform this actoin")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT,)


@router.put("/{id}",response_model=schema.Post)
def update_post(id :int, updated_post: schema.CreatePost, db: Session = Depends(get_db)
                ,current_user:int = Depends(oauth.get_current_user)):
    #cursor.execute(""" UPDATE posts SET name = %s , content = %s , published_on = %s WHERE id = %s RETURNING *""",
    #               (post.title,post.content,post.published,str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    posts = post_query.first()
 
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message":f"The post with ID {id} is not found"})
        
    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you are not autherised to perform this actoin")
        
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    
    return post_query.first()
    
