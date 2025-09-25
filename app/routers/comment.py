from fastapi import APIRouter
from app.crud import comment as crud_comment

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/{author_name}/{post_id}")
def add_comment(author_name: str, post_id: str, payload: dict):
    content = payload.get("content")
    return crud_comment.add_comment(author_name, post_id, content)
