from sqlalchemy import Column, String

from app.repository.models.base_class import Base


class Item(Base):
    __tablename__ = "item"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
