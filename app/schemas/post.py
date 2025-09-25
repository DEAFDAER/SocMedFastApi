from pydantic import BaseModel


class PostCreate(BaseModel):
    content: str


class PostResponse(BaseModel):
    element_id_property: str
    content: str
    created_at: str
    author_name: str | None = None
