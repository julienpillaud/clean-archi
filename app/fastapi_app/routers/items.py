from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.entities.item import Item, ItemCreate, ItemUpdate
from app.interfaces.repository import IItemRepository
from app.repository.dependencies import Entity, repository_provider
from app.use_cases.items import ItemManager

router = APIRouter(prefix="/items", tags=["items"])

repository_provider.entity = Entity.ITEM
Repository = Annotated[IItemRepository, Depends(repository_provider)]


@router.post("/")
def create_item(repository: Repository, create_data: ItemCreate) -> Item:
    if _ := ItemManager.get_by_name(repository, item_name=create_data.name):
        raise HTTPException(
            status_code=400,
            detail="The item with this name already exists",
        )
    return ItemManager.create(repository, create_data=create_data)


@router.get("/")
def read_items(repository: Repository) -> list[Item]:
    return ItemManager.get_multi(repository)


@router.get("/{item_id}")
def read_item(repository: Repository, item_id: int) -> Item:
    if item := ItemManager.get(repository, obj_id=item_id):
        return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{item_id}")
def update(repository: Repository, item_id: int, update_data: ItemUpdate) -> Item:
    if item := ItemManager.get(repository, obj_id=item_id):
        return ItemManager.update(repository, obj=item, update_data=update_data)
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}")
def delete(repository: Repository, item_id: int) -> Item:
    if item := ItemManager.get(repository, obj_id=item_id):
        return ItemManager.delete(repository, obj=item)
    raise HTTPException(status_code=404, detail="Item not found")
