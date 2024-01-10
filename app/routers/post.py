from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, oauth2, schemas
from ..database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("", response_model=List[schemas.PostResponse])
@router.get("", response_model=List[schemas.VotedPost])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    ## Defaults to INNER JOIN
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    )
    return posts


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(
    post: schemas.PostRequest,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """insert into posts (title, content, published)
    #                               values (%s, %s, %s) returning * """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()

    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.VotedPost)  # Path parameter
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""select * from posts where id = %s""", (str(id)))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id).filter(models.Post.id == id).first()
    )
    print(post)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found.",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)  # Path parameter
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""delete from posts where id = %s returning id""", (str(id)))
    # post_id = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found.",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action.",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)  # Path parameter
def update_post(
    id: int,
    post: schemas.PostRequest,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """update posts
    #           set title = %s,
    #               content = %s,
    #               published = %s
    #         where id = %d
    #     returning *""",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found.",
        )

    if updated_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action.",
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
