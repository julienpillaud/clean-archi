import uuid

from app.entities.item import Item, ItemCreate, ItemUpdate
from app.interfaces.repository import IItemRepository

fake_item_database = {
    Item(id="1", name="Item1", description="item 1"),
    Item(id="2", name="Item2", description="item 2"),
}


class FakeItemRepository(IItemRepository):
    def __init__(self, database: set[Item]) -> None:
        self.database = database

    def create(self, create_data: ItemCreate) -> Item:
        item = Item(
            id=str(uuid.uuid4()),
            name=create_data.name,
            description=create_data.description,
        )
        self.database.add(item)
        return item

    def get(self, obj_id: str) -> Item | None:
        item = [x for x in self.database if x.id == obj_id]
        return item[0] if item else None

    def get_by_name(self, item_name: str) -> Item | None:
        item = [x for x in self.database if x.name == item_name]
        return item[0] if item else None

    def get_multi(self) -> list[Item]:
        return list(self.database)

    def update(self, obj: Item, update_data: ItemUpdate) -> Item:
        obj_dict = obj.model_dump(exclude={"id"})
        update_data_dict = update_data.model_dump(exclude_unset=True)
        data = obj_dict | update_data_dict

        self.database.remove(obj)

        item = Item(
            id=obj.id,
            name=data["name"],
            description=data["description"],
        )
        self.database.add(item)
        return item

    def delete(self, obj: Item) -> Item:
        self.database.remove(obj)
        return obj
