from enum import StrEnum, auto

from app.interfaces.repository import IItemRepository
from app.repository.sql.items import SQLiteItemRepository
from app.repository.sql.session import SessionLocal
from tests.repository import FakeItemRepository, fake_database


class RepositoryProviderError(Exception):
    pass


class Entity(StrEnum):
    ITEM = auto()


class BaseRepositoryProvider:
    def __init__(self) -> None:
        self.entity: Entity | None = None


class RepositoryProvider(BaseRepositoryProvider):
    _mapping = {Entity.ITEM: SQLiteItemRepository}

    def __call__(self) -> IItemRepository:
        if self.entity and (repository := self._mapping.get(self.entity)):
            session = SessionLocal()
            return repository(session=session)

        raise RepositoryProviderError("Can't defined a repository. Check entity")


repository_provider = RepositoryProvider()


class TestingRepositoryProvider(BaseRepositoryProvider):
    _mapping = {Entity.ITEM: FakeItemRepository}

    def __call__(self) -> IItemRepository:
        if self.entity and (repository := self._mapping.get(self.entity)):
            return repository(database=fake_database)

        raise RepositoryProviderError("Can't defined a repository. Check entity")


testing_repository_provider = TestingRepositoryProvider()
