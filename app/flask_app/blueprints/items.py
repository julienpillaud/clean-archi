from http import HTTPStatus

from flask import Blueprint, Response, current_app, json, jsonify, request
from pydantic import ValidationError

from app.entities.item import ItemCreate, ItemUpdate
from app.repository.dependencies import Entity, repository_provider
from app.use_cases.items import ItemManager

blueprint = Blueprint(name="items", import_name=__name__, url_prefix="/items")

repository_provider.entity = Entity.ITEM


@blueprint.post("/")
def create_item() -> Response:
    try:
        create_data = ItemCreate(**request.get_json())
    except ValidationError as err:
        return Response(
            response=json.dumps({"detail": err.errors()}),
            status=HTTPStatus.UNPROCESSABLE_ENTITY,
            mimetype="application/json",
        )

    repository = current_app.config["repository_provider"]()

    if _ := ItemManager.get_by_name(repository, item_name=create_data.name):
        return Response(
            response=json.dumps({"detail": "The item with this name already exists"}),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    item = ItemManager.create(repository, create_data=create_data)
    return jsonify(item.model_dump())


@blueprint.get("/")
def read_items() -> Response:
    repository = current_app.config["repository_provider"]()

    items = ItemManager.get_multi(repository)
    items_json = [item.model_dump() for item in items]
    return jsonify(items_json)


@blueprint.get("/<item_id>")
def read_item(item_id: str) -> Response:
    repository = current_app.config["repository_provider"]()

    if item := ItemManager.get(repository, obj_id=item_id):
        return jsonify(item.model_dump())

    return Response(
        response=json.dumps({"detail": "Item not found"}),
        status=HTTPStatus.NOT_FOUND,
        mimetype="application/json",
    )


@blueprint.put("/<item_id>")
def update(item_id: str) -> Response:
    try:
        update_data = ItemUpdate(**request.get_json())
    except ValidationError as err:
        return Response(
            response=json.dumps({"detail": err.errors()}),
            status=HTTPStatus.UNPROCESSABLE_ENTITY,
            mimetype="application/json",
        )

    repository = current_app.config["repository_provider"]()

    if item := ItemManager.get(repository, obj_id=item_id):
        item = ItemManager.update(repository, obj=item, update_data=update_data)
        return jsonify(item.model_dump())

    return Response(
        response=json.dumps({"detail": "Item not found"}),
        status=HTTPStatus.NOT_FOUND,
        mimetype="application/json",
    )


@blueprint.delete("/<item_id>")
def delete(item_id: str) -> Response:
    repository = current_app.config["repository_provider"]()

    if item := ItemManager.get(repository, obj_id=item_id):
        item = ItemManager.delete(repository, obj=item)
        return jsonify(item.model_dump())

    return Response(
        response=json.dumps({"detail": "Item not found"}),
        status=HTTPStatus.NOT_FOUND,
        mimetype="application/json",
    )
