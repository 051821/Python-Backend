#6 for routers

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import List
from .. import model, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db

from sqlalchemy import func

router = APIRouter(
    prefix = "/posts" ,  # for global prefix
    tags = ['Post']
)

@router.post("/", response_model=schemas.PostResponse, status_code=201)  # after creating oauth verification so after verification user can post
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # db session is injected via dependency injection (Depends) this is how we interact with the database in our route handlers
    # we create a new Post object using the SQLAlchemy model and the data from the request (schemas.PostCreate)

    print(current_user)
    db_post = model.Post(**post.dict(),user_id=current_user.id)
    # db_post = model.Post(   # ✅ FIXED
    #     title=post.title,
    #     content=post.content,
    #     published=post.published,
    #     # to link user with post after oauth verification implementation
    #     user_id = current_user.id
    # )


    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


# =========================
# ✅ READ ALL POSTS
# =========================4
@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10,search: str = ""):

    #posts = db.query(model.Post).filter(model.post.title.contains(search)).limit(limit).all()   # ✅ FIXED
                                                                                    #left outer join
    results = db.query(model.Post, func.count(model.Vote.post_id).label("likes")).join(model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(model.Post.id).filter(model.Post.title.contains(search)).order_by(model.Post.title.contains(search)).limit(limit).all()
    print(results)
    return  results


# =========================
# ✅ READ SINGLE POST
# =========================
#@router.get("/{post_id}", response_model=schemas.PostResponse)
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):

    #post = db.query(model.Post).filter(model.Post.id == post_id).first()
    post = db.query(model.Post, func.count(model.Vote.post_id).label("likes")).join(model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(model.Post.id).filter(model.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


# =========================
# ✅ DELETE POST
# =========================
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    post = db.query(model.Post).filter(model.Post.id == post_id)

    if post.first() is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")

    post.delete(synchronize_session=False)
    db.commit()

    return {"message": "Post deleted successfully"}


# =========================
# ✅ UPDATE POST
# =========================
@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(model.Post).filter(model.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()