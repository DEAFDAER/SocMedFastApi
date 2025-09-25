from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from app.config import config  # <-- make sure this is imported first
from neomodel import db
from neo4j.exceptions import AuthError, ServiceUnavailable
from app.routers import person, post, comment
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="FastAPI + Neo4j")

app.include_router(person.router)
app.include_router(post.router)
app.include_router(comment.router)

# Serve a minimal frontend directory at /frontend
app.mount("/frontend", StaticFiles(directory="./frontend", html=True), name="frontend")


@app.get("/")
def read_root():
    return {"message": "FastAPI + Neo4j backend is running"}


@app.get("/health")
def health_check():
    """Simple health check used by Render or other platform health probes.

    Returns 200 OK if the application can reach Neo4j (best-effort). If the DB
    cannot be reached this will still return 503 so orchestrators can detect
    an unhealthy instance.
    """
    try:
        db.cypher_query("RETURN 1")
        return {"status": "ok"}
    except Exception:
        from fastapi import HTTPException

        raise HTTPException(status_code=503, detail="db-unreachable")


@app.get("/favicon.ico")
def favicon():
    # Return a minimal SVG favicon to avoid browser 404 noise during development
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">'
        '<rect width="16" height="16" fill="#111827" rx="3"/>'
        '<text x="50%" y="50%" font-size="9" fill="#ffffff" dominant-baseline="middle" text-anchor="middle">API</text>'
        '</svg>'
    )
    return Response(content=svg, media_type="image/svg+xml")


@app.get("/dash")
def dash_redirect():
    """Redirect legacy /dash requests to the static frontend mount at /frontend/"""
    return RedirectResponse(url="/frontend/")

@app.on_event("startup")
def startup_db_check():
    try:
        db.cypher_query("RETURN 1")
        print("[✅] Neo4j connection successful!")
    except AuthError:
        print("[❌] Authentication failed: Check username/password.")
        raise
    except ServiceUnavailable:
        print("[❌] Cannot connect: Is Neo4j running?")
        raise
    except Exception as e:
        print(f"[❌] Neo4j connection failed: {e}")
        raise
