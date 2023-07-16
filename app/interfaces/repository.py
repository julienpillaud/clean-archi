from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

from app.entities.item import Item, ItemCreate, ItemUpdate

SchemaType = TypeVar("SchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class IBaseRepository(ABC, Generic[SchemaType, CreateSchemaType, UpdateSchemaType]):
    """
    Abstract base class for repository

    Defined methods for common CRUD operations
    """

    @abstractmethod
    def create(self, create_data: CreateSchemaType) -> SchemaType:
        """Create a new ressource"""

    @abstractmethod
    def get(self, obj_id: str) -> SchemaType | None:
        """Get a ressource by its id"""

    @abstractmethod
    def get_multi(self) -> list[SchemaType]:
        """Get all ressources"""

    @abstractmethod
    def update(self, obj: SchemaType, update_data: UpdateSchemaType) -> SchemaType:
        """Update a resource"""

    @abstractmethod
    def delete(self, obj: SchemaType) -> SchemaType:
        """Delete a ressource"""


class IItemRepository(IBaseRepository[Item, ItemCreate, ItemUpdate]):
    """
    Abstract class for Item repository

    Defined specific methods for item schema
    """

    @abstractmethod
    def get_by_name(self, item_name: str) -> Item | None:
        """Get an item by its name"""
