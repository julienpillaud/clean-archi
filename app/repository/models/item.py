from sqlalchemy import Column, Integer, String

from app.repository.models.base_class import Base


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)