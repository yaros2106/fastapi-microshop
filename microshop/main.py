from fastapi import (
    FastAPI,
    Request,
)

from items_views import router as items_router
from users.views import router as users_router

app = FastAPI(
    title="FastAPI-Micro-shop",
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


app.include_router(items_router)
app.include_router(users_router)
