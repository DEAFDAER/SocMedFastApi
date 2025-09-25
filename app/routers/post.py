from fastapi import APIRouter
from app.schemas.post import PostCreate, PostResponse
from app.crud import post as crud_post
from app.models.post import Post

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/{author_name}")
def create_post(author_name: str, payload: PostCreate):
    return crud_post.create_post(author_name, payload)


@router.get("/")
def list_posts():
    return crud_post.list_posts()


@router.get("/{node_id}")
def get_post(node_id: str):
    return crud_post.get_post(node_id)
