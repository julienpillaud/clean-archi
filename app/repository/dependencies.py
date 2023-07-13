from enum import StrEnum, auto

from app.interfaces.repository import IItemRepository
from app.repository.sql.items import SQLiteItemRepository
from app.repository.sql.session import SessionLocal


class RepositoryProviderError(Exception):
    pass


class Entity(StrEnum):
    ITEM = auto()


class RepositoryProvider:
    _mapping = {Entity.ITEM: SQLiteItemRepository}

    def __init__(self) -> None:
        self.entity: Entity | None = None
        self.session = SessionLocal

    def __call__(self) -> IItemRepository:
        if self.entity and (repository := self._mapping.get(self.entity)):
            return repository(session=self.session())
        raise RepositoryProviderError("Can't defined a repository. Check entity")


repository_provider = RepositoryProvider()
