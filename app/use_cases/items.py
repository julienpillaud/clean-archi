from app.entities.item import Item, ItemCreate, ItemUpdate
from app.interfaces.repository import IItemRepository


class ItemManager:
    @staticmethod
    def create(repository: IItemRepository, create_data: ItemCreate) -> Item:
        return repository.create(create_data=create_data)

    @staticmethod
    def get(repository: IItemRepository, obj_id: str) -> Item | None:
        return repository.get(obj_id=obj_id)

    @staticmethod
    def get_by_name(repository: IItemRepository, item_name: str) -> Item | None:
        return repository.get_by_name(item_name=item_name)

    @staticmethod
    def get_multi(repository: IItemRepository) -> list[Item]:
        return repository.get_multi()

    @staticmethod
    def update(repository: IItemRepository, obj: Item, update_data: ItemUpdate) -> Item:
        return repository.update(obj=obj, update_data=update_data)

    @staticmethod
    def delete(repository: IItemRepository, obj: Item) -> Item:
        return repository.delete(obj=obj)
