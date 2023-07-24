from enum import StrEnum, auto

from app.interfaces.repository import IItemRepository
from app.repository.mongodb.client import database  # noqa
from app.repository.mongodb.items import MongoItemRepository  # noqa
from app.repository.sql.items import SQLiteItemRepository  # noqa
from app.repository.sql.session import SessionLocal  # noqa
from tests.fake_repository import FakeItemRepository, fake_database


class RepositoryProviderError(Exception):
    pass


class Entity(StrEnum):
    ITEM = auto()


class BaseRepositoryProvider:
    def __init__(self) -> None:
        self.entity: Entity | None = None


class RepositoryProvider(BaseRepositoryProvider):
    # This is where the code changes according to the repository
    # we want to use for this project only.

    # _mapping = {Entity.ITEM: SQLiteItemRepository}
    _mapping = {Entity.ITEM: MongoItemRepository}

    def __call__(self) -> IItemRepository:
        if self.entity and (repository := self._mapping.get(self.entity)):
            # return repository(session=SessionLocal)
            return repository(database=database)

        raise RepositoryProviderError("Can't defined a repository. Check entity")


repository_provider = RepositoryProvider()


class TestingRepositoryProvider(BaseRepositoryProvider):
    _mapping = {Entity.ITEM: FakeItemRepository}

    def __call__(self) -> IItemRepository:
        if self.entity and (repository := self._mapping.get(self.entity)):
            return repository(database=fake_database)

        raise RepositoryProviderError("Can't defined a repository. Check entity")


testing_repository_provider = TestingRepositoryProvider()
