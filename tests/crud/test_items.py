import pytest

from app.entities.item import Item, ItemCreate, ItemUpdate
from app.interfaces.repository import IItemRepository
from app.use_cases.items import ItemManager


@pytest.mark.entity("item")
def test_create_item(repository: IItemRepository) -> None:
    item_in = ItemCreate(name="Item1", description="item 1")
    item = ItemManager.create(repository, create_data=item_in)

    assert item.name == item_in.name
    assert item.description == item_in.description


@pytest.mark.entity("item")
def test_read_item(repository: IItemRepository, created_item: Item) -> None:
    item = ItemManager.get(repository, obj_id=created_item.id)

    assert item
    assert item.id == created_item.id
    assert item.name == created_item.name
    assert item.description == created_item.description


@pytest.mark.entity("item")
def test_read_items(repository: IItemRepository, created_item: Item) -> None:
    items = ItemManager.get_multi(repository)

    assert len(items) > 1


@pytest.mark.entity("item")
def test_update_item(repository: IItemRepository, created_item: Item) -> None:
    item_in = ItemUpdate(description="updated description")
    item = ItemManager.update(repository, obj=created_item, update_data=item_in)

    assert item.id == created_item.id
    assert item.name == created_item.name
    assert item.description == item_in.description


@pytest.mark.entity("item")
def test_delete_item(repository: IItemRepository, created_item: Item) -> None:
    item = ItemManager.delete(repository, obj=created_item)

    assert item.id == created_item.id
    assert item.name == created_item.name
    assert item.description == created_item.description
