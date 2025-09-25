from fastapi import HTTPException
from app.models.post import Post
from app.models.person import Person
from app.schemas.post import PostCreate
import time
import socket
from neo4j import exceptions as neo4j_exceptions


def _with_retry(fn, retries=2, backoff=0.5):
    """Run a DB operation with a small retry for transient errors.

    Returns the function result or raises HTTPException(503) on persistent failures.
    """
    last_exc = None
    for attempt in range(retries + 1):
        try:
            return fn()
        except (neo4j_exceptions.ServiceUnavailable, neo4j_exceptions.SessionExpired, OSError, socket.error) as e:
            last_exc = e
            # brief backoff before retrying
            time.sleep(backoff * (attempt + 1))
    # If we get here, all retries failed
    raise HTTPException(status_code=503, detail=f"Database unavailable: {last_exc}")


def create_post(author_name: str, data: PostCreate):
    def _op():
        author = Person.nodes.get_or_none(name=author_name)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

        post = Post(content=data.content).save()
        author.posts.connect(post)
        # return a serializable dict including author
        d = post.to_dict()
        d["author_name"] = author.name
        return d

    return _with_retry(_op)


def list_posts():
    def _op():
        posts = Post.nodes.all()
        result = []
        for p in posts:
            d = p.to_dict()
            authors = [n for n in p.author]
            d["author_name"] = authors[0].name if authors else None
            result.append(d)
        return result

    return _with_retry(_op)


def get_post(node_id: str):
    def _op():
        post = Post.nodes.get_or_none(element_id=node_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        d = post.to_dict()
        authors = [n for n in post.author]
        d["author_name"] = authors[0].name if authors else None
        return d

    return _with_retry(_op)
