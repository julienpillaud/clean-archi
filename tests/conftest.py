import pytest
from pytest import FixtureRequest

from app.entities.item import Item
from app.interfaces.repository import IItemRepository
from app.repository.dependencies import testing_repository_provider
from tests.fake_repository import fake_item_database


@pytest.fixture(autouse=True)
def init_repository(request: FixtureRequest) -> None:
    if marker := request.node.get_closest_marker("entity"):
        entity = marker.args[0]
        testing_repository_provider.entity = entity


@pytest.fixture
def repository() -> IItemRepository:
    return testing_repository_provider()


@pytest.fixture
def created_item() -> Item:
    return next(iter(fake_item_database))
