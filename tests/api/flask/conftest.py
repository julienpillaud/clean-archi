import pytest
from flask.testing import FlaskClient

from app.flask_app.main import app
from app.repository.dependencies import testing_repository_provider


@pytest.fixture
def client() -> FlaskClient:
    app.config["repository_provider"] = testing_repository_provider
    app.config.update({"TESTING": True})
    return app.test_client()
