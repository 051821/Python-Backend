from fastapi import FastAPI, Depends, HTTPException, APIRouter
from .. import model, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import oauth2

router = APIRouter(
    prefix = "/vote" ,  # for global prefix
    tags = ['Vote']
)


@router.post("/", status_code=201)
def vote(
    vote: schemas.PostOut,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    post =db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")


    vote_query = db.query(model.Vote).filter(
        model.Vote.post_id == vote.post_id,
        model.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=409, detail="User already voted on the post")

        new_vote = model.Vote(
            post_id=vote.post_id,
            user_id=current_user.id
        )
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote"}