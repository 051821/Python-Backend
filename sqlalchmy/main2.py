# 4
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import utils
import time 
from . import model, schemas   # ✅ use model (singular)
from .database import SessionLocal, engine, Base, get_db
from . Routers  import post,user,auth, vote

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = ["*"]
# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Creating tables...")

# Create tables
Base.metadata.create_all(bind=engine)
print(Base.metadata.tables.keys())

from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT current_database();"))
    print("ORM DB:", result.fetchone())

    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
    print("ORM Tables:", result.fetchall())

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def read_root():
    return {"message": "FastAPI + PostgreSQL working"}
# 🔥 Dependency: Get DB session per request



# =========================
# ✅ CREATE POST
# =========================
                     # pydantic schema for request body, response model for response validation, status code for successful creation
# @app.post("/posts/", response_model=schemas.PostResponse, status_code=201)
# def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
#     # db session is injected via dependency injection (Depends) this is how we interact with the database in our route handlers
#     # we create a new Post object using the SQLAlchemy model and the data from the request (schemas.PostCreate)

#     db_post = model.Post(   # ✅ FIXED
#         title=post.title,
#         content=post.content,
#         published=post.published
#     )


#     db.add(db_post)
#     db.commit()
#     db.refresh(db_post)

#     return db_post


# # =========================
# # ✅ READ ALL POSTS
# # =========================
# @app.get("/posts/", response_model=list[schemas.PostResponse])
# def get_posts(db: Session = Depends(get_db)):

#     posts = db.query(model.Post).all()   # ✅ FIXED
#     return posts


# # =========================
# # ✅ READ SINGLE POST
# # =========================
# @app.get("/posts/{post_id}", response_model=schemas.PostResponse)
# def get_post(post_id: int, db: Session = Depends(get_db)):

#     post = db.query(model.Post).filter(model.Post.id == post_id).first()

#     if post is None:
#         raise HTTPException(status_code=404, detail="Post not found")

#     return post


# # =========================
# # ✅ DELETE POST
# # =========================
# @app.delete("/posts/{post_id}")
# def delete_post(post_id: int, db: Session = Depends(get_db)):

#     post = db.query(model.Post).filter(model.Post.id == post_id)

#     if post.first() is None:
#         raise HTTPException(status_code=404, detail="Post not found")

#     post.delete(synchronize_session=False)
#     db.commit()

#     return {"message": "Post deleted successfully"}


# # =========================
# # ✅ UPDATE POST
# # =========================
# @app.put("/posts/{post_id}", response_model=schemas.PostResponse)
# def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

#     post_query = db.query(model.Post).filter(model.Post.id == post_id)
#     post = post_query.first()

#     if post is None:
#         raise HTTPException(status_code=404, detail="Post not found")

#     post_query.update(updated_post.dict(), synchronize_session=False)
#     db.commit()

#     return post_query.first()



## USER 

#                     # response from server
# @app.post("/users", response_model=schemas.UserResponse)
# def create_user(user: schemas.usercreate, db: Session = Depends(get_db)):

#     user_dict = user.dict()
#     user_dict["password"] = utils.hash(user.password)

#     new_user = model.User(**user_dict)

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user

# @app.get('/user/{id}',response_model=schemas.UserResponse)
# def get_user(id:int, db: Session = Depends(get_db)):
#     user = db.query(model.User).filter(model.User.id == id).first()

#     if not user:
#         raise HTTPException(status_code=404, detail = "USer not found")
    
#     return user

    

