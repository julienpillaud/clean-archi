from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from pytest import FixtureRequest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.entities.item import Item, ItemCreate
from app.fastapi_app.main import app
from app.interfaces.repository import IItemRepository
from app.repository.dependencies import repository_provider

# import Base class and all models before creating tables
from app.repository.models import base

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override session for tests
repository_provider.session = SessionLocal

base.Base.metadata.create_all(bind=engine)


@pytest.fixture(autouse=True)
def repository_entity(request: FixtureRequest) -> None:
    if marker := request.node.get_closest_marker("entity"):
        entity = marker.args[0]
        repository_provider.entity = entity


@pytest.fixture
def repository() -> IItemRepository:
    return repository_provider()


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def created_item(repository: IItemRepository) -> Item:
    """Populate the database with 2 items"""
    item_1 = ItemCreate(name="Item1", description="item 1")
    item_2 = ItemCreate(name="Item2", description="item 2")
    repository.create(item_1)
    return repository.create(item_2)
