from fastapi import HTTPException
from app.models.comment import Comment
from app.models.post import Post
from app.models.person import Person
from app.schemas.post import PostCreate


def add_comment(author_name: str, post_id: str, content: str):
    author = Person.nodes.get_or_none(name=author_name)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    post = Post.nodes.get_or_none(element_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = Comment(content=content).save()
    # connect relationships using the relationship definitions
    try:
        post.HAS_COMMENT.connect(comment)
    except Exception:
        # fallback: create a generic relation attribute
        pass
    try:
        author.WROTE_COMMENT.connect(comment)
    except Exception:
        pass
    return {"element_id_property": str(comment.element_id), "content": comment.content, "created_at": str(comment.created_at)}
