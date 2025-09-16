from fastapi import (
    FastAPI,
    Request,
)
from pydantic import (
    EmailStr,
    BaseModel,
)


class CreateUser(BaseModel):
    email: EmailStr


class Books(BaseModel):
    title: str
    author: str


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


@app.get("/items/latest/")
def get_latest_item() -> dict[str, dict[str, str]]:
    return {
        "item": {
            "id": "0",
            "name": "latest",
        },
    }


@app.get("/items/{item_id}/")
def get_item_by_id(item_id: int) -> dict[str, dict[str, int]]:
    return {
        "item": {
            "id": item_id,
        },
    }


@app.get("/items/")
def list_items() -> list[str]:
    return [
        "item1",
        "item2",
    ]


@app.get("/hello/")
def hello(name: str = "World") -> dict[str, str]:
    name = name.strip().title()
    return {"message": f"Hello {name}!"}


@app.post("/users")
def create_user(user: CreateUser) -> dict[str, str]:
    return {
        "message": "New user created",
        "email": user.email,
    }


@app.get("/calc/add")
def add(a: int, b: int) -> dict[str, int]:
    return {"result": a + b}
