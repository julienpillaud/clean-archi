import http

import pytest
from fastapi.testclient import TestClient

from app.entities.item import Item


@pytest.mark.entity("item")
def test_create_item(client: TestClient) -> None:
    data = {"name": "FastAPI Item", "description": "item"}
    response = client.post("/items", json=data)

    assert response.status_code == http.HTTPStatus.OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert "id" in content


@pytest.mark.entity("item")
def test_create_existing_item(client: TestClient, created_item: Item) -> None:
    data = {"name": created_item.name, "description": created_item.description}
    response = client.post("/items", json=data)

    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    content = response.json()
    assert content["detail"] == "The item with this name already exists"


@pytest.mark.entity("item")
def test_create_bad_data(client: TestClient) -> None:
    data = {"bad_key": ""}
    response = client.post("/items", json=data)

    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
    content = response.json()
    assert "detail" in content
    detail = content["detail"][0]
    assert detail["type"] == "assertion_error"
    assert detail["msg"] == "Assertion failed, At least one filed is required"


@pytest.mark.entity("item")
def test_read_item(client: TestClient, created_item: Item) -> None:
    response = client.get(f"/items/{created_item.id}")

    assert response.status_code == http.HTTPStatus.OK
    content = response.json()
    assert content["id"] == created_item.id
    assert content["name"] == created_item.name
    assert content["description"] == created_item.description


@pytest.mark.entity("item")
def test_read_bad_item(client: TestClient) -> None:
    response = client.get("/items/0")

    assert response.status_code == http.HTTPStatus.NOT_FOUND
    content = response.json()
    assert content["detail"] == "Item not found"


@pytest.mark.entity("item")
def test_read_items(client: TestClient) -> None:
    response = client.get("/items")

    assert response.status_code == http.HTTPStatus.OK
    content = response.json()
    assert len(content) > 1
    for result in content:
        assert "id" in result
        assert "name" in result
        assert "description" in result


@pytest.mark.entity("item")
def test_update_item(client: TestClient, created_item: Item) -> None:
    data = {"name": "Toto"}
    response = client.put(f"/items/{created_item.id}", json=data)

    assert response.status_code == http.HTTPStatus.OK
    content = response.json()
    assert content["id"] == created_item.id
    assert content["name"] == data["name"]


@pytest.mark.entity("item")
def test_update_bad_item(client: TestClient) -> None:
    data = {"name": "Toto"}
    response = client.put("/items/0", json=data)

    assert response.status_code == http.HTTPStatus.NOT_FOUND
    content = response.json()
    assert content["detail"] == "Item not found"


@pytest.mark.entity("item")
def test_update_bad_data(client: TestClient, created_item: Item) -> None:
    data = {"not_name_or_description": ""}
    response = client.put(f"/items/{created_item.id}", json=data)

    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
    content = response.json()
    assert "detail" in content
    detail = content["detail"][0]
    assert detail["type"] == "assertion_error"
    assert detail["msg"] == "Assertion failed, At least one filed is required"


@pytest.mark.entity("item")
def test_delete_item(client: TestClient, created_item: Item) -> None:
    response = client.delete(f"items/{created_item.id}")

    assert response.status_code == http.HTTPStatus.OK
    content = response.json()
    assert content["id"] == created_item.id
    assert content["name"] == created_item.name
    assert content["description"] == created_item.description


@pytest.mark.entity("item")
def test_delete_bad_item(client: TestClient) -> None:
    response = client.delete("items/0")

    assert response.status_code == http.HTTPStatus.NOT_FOUND
    content = response.json()
    assert content["detail"] == "Item not found"
