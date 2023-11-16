from fastapi import FastAPI,HTTPException,status,Response,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import schema,models,database,oauth

router = APIRouter(tags=['vote'])

@router.post("/vote")

def vote(votes: schema.vote,db: Session = Depends(database.get_db),
          current_user: int = Depends(oauth.get_current_user)):
    
    find_post = db.query(models.Post).filter(models.Post.id == votes.posts_id).first()
    
    if not find_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with ID: {votes.posts_id} doesnt exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == votes.posts_id, 
                                               models.Vote.user_id == current_user.id)
    
    found_vote= vote_query.first()
    
    if (votes.dir == 1):
        if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                 detail=f"The user with ID:{current_user.id} has already like the post with ID: {votes.posts_id}")
            
        new_vote = models.Vote(post_id= votes.posts_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        
        return {"message":"The vote added succesfully"}
    
    else:
        
         if not found_vote:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The vote doesnt exist')
        
         vote_query.delete(synchronize_session=False)
         db.commit()
        
         return {"message":"The vote deleted succesfully"}