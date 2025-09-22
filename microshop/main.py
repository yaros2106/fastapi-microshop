from fastapi import (
    FastAPI,
    Request,
)

from api_v1 import router as api_v1_router
from app_lifespan import lifespan

from items_views import router as items_router

app = FastAPI(
    title="FastAPI-Micro-shop",
    lifespan=lifespan,
)


@app.get("/")
def read_root(request: Request) -> dict[str, str]:
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "docs": str(docs_url),
    }


app.include_router(api_v1_router)
app.include_router(items_router)
