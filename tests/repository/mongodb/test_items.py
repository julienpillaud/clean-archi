from bson import ObjectId
from pymongo.database import Database

from app.entities.item import Item, ItemCreate, ItemUpdate
from app.repository.mongodb.items import ItemSchema, MongoItemRepository


def test_create(database: Database[ItemSchema]) -> None:
    repo = MongoItemRepository(database)
    item_create = ItemCreate(name="Item test", description="item test")
    repo.create(create_data=item_create)

    item = database.item.find_one({"name": item_create.name})

    assert item
    assert item["name"] == item_create.name
    assert item["description"] == item_create.description


def test_get(database: Database[ItemSchema], items: list[Item]) -> None:
    item_in = items[0]

    repo = MongoItemRepository(database)
    item = repo.get(obj_id=item_in.id)

    assert item
    assert item.id == item_in.id
    assert item.name == item_in.name
    assert item.description == item_in.description


def test_get_by_name(database: Database[ItemSchema], items: list[Item]) -> None:
    item_in = items[0]

    repo = MongoItemRepository(database)
    item = repo.get_by_name(item_name=item_in.name)

    assert item
    assert item.id == item_in.id
    assert item.name == item_in.name
    assert item.description == item_in.description


def test_get_multi(database: Database[ItemSchema], items: list[Item]) -> None:
    repo = MongoItemRepository(database)
    db_items = repo.get_multi()

    assert db_items == items


def test_update(database: Database[ItemSchema], items: list[Item]) -> None:
    item_in = items[0]

    repo = MongoItemRepository(database)
    item_update = ItemUpdate(description="updated description")
    repo.update(obj=item_in, update_data=item_update)

    item = database.item.find_one({"_id": ObjectId(item_in.id)})

    assert item
    assert item["name"] == item_in.name
    assert item["description"] == item_update.description


def test_delete(database: Database[ItemSchema], items: list[Item]) -> None:
    item_in = items[0]

    repo = MongoItemRepository(database)
    repo.delete(item_in)

    item = database.item.find_one({"_id": ObjectId(item_in.id)})

    assert not item
