from collections.abc import Iterator

import pytest
from pymongo import MongoClient
from pymongo.database import Database

from app.entities.item import Item, ItemCreate
from app.repository.mongodb.items import ItemSchema

MONGODB_DATABASE = "test"


@pytest.fixture
def database() -> Iterator[Database[ItemSchema]]:
    client: MongoClient[ItemSchema] = MongoClient("mongodb://localhost:27017/")
    yield client[MONGODB_DATABASE]
    client.drop_database(MONGODB_DATABASE)
    client.close()


@pytest.fixture
def items(database: Database[ItemSchema]) -> Iterator[list[Item]]:
    item_1 = ItemCreate(name="Item1", description="item 1")
    item_2 = ItemCreate(name="Item2", description="item 2")
    collection = database.item

    items = collection.insert_many(
        [
            ItemSchema(name=item_1.name, description=item_1.description),
            ItemSchema(name=item_2.name, description=item_2.description),
        ]
    )
    inserted_ids = [str(x) for x in items.inserted_ids]

    yield [
        Item(id=inserted_ids[0], name=item_1.name, description=item_1.description),
        Item(id=inserted_ids[1], name=item_2.name, description=item_2.description),
    ]

    collection.delete_many({})
