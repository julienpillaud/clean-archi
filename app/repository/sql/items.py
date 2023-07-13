from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.entities.item import Item, ItemCreate, ItemUpdate
from app.interfaces.repository import IItemRepository
from app.repository.models import item


class SQLiteItemRepository(IItemRepository):
    def __init__(self, session: Session):
        self.session = session
        self.model = item.Item

    def create(self, create_data: ItemCreate) -> Item:
        db_obj = self.model(
            name=create_data.name,
            description=create_data.description,
        )
        with self.session as session:
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)

        return Item.model_validate(db_obj)

    def get(self, obj_id: int) -> Item | None:
        filter_ = self.model.id == obj_id
        with self.session as session:
            obj = session.query(self.model).filter(filter_).first()

        return Item.model_validate(obj) if obj else None

    def get_by_name(self, item_name: str) -> Item | None:
        filter_ = self.model.name == item_name
        with self.session as session:
            obj = session.query(self.model).filter(filter_).first()

        return Item.model_validate(obj) if obj else None

    def get_multi(self) -> list[Item]:
        with self.session as session:
            objs = session.query(self.model).all()

        return [Item.model_validate(x) for x in objs]

    def update(self, obj: Item, update_data: ItemUpdate) -> Item:
        db_obj = self.session.get(self.model, obj.id)
        db_obj_data = jsonable_encoder(db_obj)
        data = update_data.model_dump(exclude_unset=True)

        for field in db_obj_data:
            if field in data:
                setattr(db_obj, field, data[field])

        with self.session as session:
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)

        return Item.model_validate(db_obj)

    def delete(self, obj: Item) -> Item:
        db_obj = self.session.get(self.model, obj.id)

        with self.session as session:
            session.delete(db_obj)
            session.commit()

        return Item.model_validate(db_obj)
