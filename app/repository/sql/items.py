import uuid

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.entities.item import Item, ItemCreate, ItemUpdate
from app.interfaces.repository import IItemRepository
from app.repository.models import item


class SQLiteItemRepository(IItemRepository):
    def __init__(self, session: sessionmaker[Session]):
        self.session = session
        self.model = item.Item

    def create(self, create_data: ItemCreate) -> Item:
        db_item = self.model(
            id=str(uuid.uuid4()),
            name=create_data.name,
            description=create_data.description,
        )
        with self.session() as session:
            session.add(db_item)
            session.commit()
            session.refresh(db_item)

        return Item.model_validate(db_item)

    def get(self, obj_id: str) -> Item | None:
        with self.session() as session:
            db_item = session.get(self.model, obj_id)

        return Item.model_validate(db_item) if db_item else None

    def get_by_name(self, item_name: str) -> Item | None:
        stmt = select(self.model).where(self.model.name == item_name)
        with self.session() as session:
            db_item = session.scalar(stmt)

        return Item.model_validate(db_item) if db_item else None

    def get_multi(self) -> list[Item]:
        stmt = select(self.model)
        with self.session() as session:
            db_items = session.scalars(stmt).all()

        return [Item.model_validate(x) for x in db_items]

    def update(self, obj: Item, update_data: ItemUpdate) -> Item:
        with self.session() as session:
            db_item = session.get(self.model, obj.id)

            db_item_data = jsonable_encoder(db_item)
            update_item_data = update_data.model_dump(exclude_unset=True)

            for field in db_item_data:
                if field in update_item_data:
                    setattr(db_item, field, update_item_data[field])

            session.add(db_item)
            session.commit()
            session.refresh(db_item)

        return Item.model_validate(db_item)

    def delete(self, obj: Item) -> Item:
        with self.session() as session:
            db_item = session.get(self.model, obj.id)
            session.delete(db_item)
            session.commit()

        return Item.model_validate(db_item)
