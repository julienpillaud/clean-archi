from dataclasses import dataclass
from typing import TypedDict

from bson import ObjectId
from pymongo.command_cursor import CommandCursor
from pymongo.database import Database

from app.entities.item import Item, ItemCreate, ItemUpdate
from app.interfaces.repository import IItemRepository


class ItemSchema(TypedDict):
    name: str | None
    description: str | None


@dataclass
class Match:
    key: str
    value: str | ObjectId


class MongoItemRepository(IItemRepository):
    collection_name = "item"

    def __init__(self, database: Database[ItemSchema]) -> None:
        self.collection = database[self.collection_name]

    def _find(self) -> CommandCursor[ItemSchema]:
        return self.collection.aggregate(
            [
                {"$set": {"id": {"$toString": "$_id"}}},
                {"$unset": "_id"},
            ]
        )

    def _find_one(self, match: Match) -> ItemSchema | None:
        cursor = self.collection.aggregate(
            [
                {"$match": {match.key: match.value}},
                {"$set": {"id": {"$toString": "$_id"}}},
                {"$unset": "_id"},
            ]
        )
        return next(cursor, None)

    def create(self, create_data: ItemCreate) -> Item:
        document = ItemSchema(**create_data.model_dump())  # type: ignore
        inserted_item = self.collection.insert_one(document)
        item = self._find_one(Match(key="_id", value=inserted_item.inserted_id))
        return Item.model_validate(item)

    def get(self, obj_id: str) -> Item | None:
        item = self._find_one(Match(key="_id", value=ObjectId(obj_id)))
        return Item.model_validate(item) if item else None

    def get_by_name(self, item_name: str) -> Item | None:
        item = self._find_one(Match(key="name", value=item_name))
        return Item.model_validate(item) if item else None

    def get_multi(self) -> list[Item]:
        return [Item.model_validate(item) for item in self._find()]

    def update(self, obj: Item, update_data: ItemUpdate) -> Item:
        obj_dict = obj.model_dump(exclude={"id"})
        update_data_dict = update_data.model_dump(exclude_unset=True)
        data = obj_dict | update_data_dict

        self.collection.replace_one({"_id": ObjectId(obj.id)}, data)

        item = self._find_one(Match(key="_id", value=ObjectId(obj.id)))
        return Item.model_validate(item)

    def delete(self, obj: Item) -> Item:
        self.collection.delete_one({"_id": ObjectId(obj.id)})
        return obj
