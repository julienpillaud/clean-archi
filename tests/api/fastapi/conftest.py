from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.fastapi_app.main import app
from app.repository.dependencies import repository_provider, testing_repository_provider


@pytest.fixture
def client() -> Iterator[TestClient]:
    app.dependency_overrides[repository_provider] = testing_repository_provider
    with TestClient(app) as test_client:
        yield test_client
