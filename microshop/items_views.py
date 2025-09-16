from typing import Annotated

from annotated_types import Ge, Le
from fastapi import APIRouter


router = APIRouter(
    tags=["Items"],
    prefix="/items",
)


@router.get("/")
def list_items() -> list[str]:
    return [
        "item1",
        "item2",
    ]


@router.get("/latest/")
def get_latest_item() -> dict[str, dict[str, str]]:
    return {
        "item": {
            "id": "0",
            "name": "latest",
        },
    }


@router.get("/{item_id}/")
def get_item_by_id(
    item_id: Annotated[
        int,
        Ge(1),
        Le(1_000_000),
    ],
) -> dict[str, dict[str, int]]:
    return {
        "item": {
            "id": item_id,
        },
    }
