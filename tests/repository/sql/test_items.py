from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text

from app.entities.item import Item, ItemCreate, ItemUpdate
from app.repository.sql.items import SQLiteItemRepository


def test_create(session_local: sessionmaker[Session]) -> None:
    repo = SQLiteItemRepository(session=session_local)
    item_create = ItemCreate(name="Item test", description="item test")
    repo.create(create_data=item_create)

    stmt = text("SELECT * FROM item WHERE name = :name")
    with session_local() as session:
        row = session.execute(stmt, {"name": item_create.name}).first()

    assert row
    assert row.name == item_create.name
    assert row.description == item_create.description


def test_get(session_local: sessionmaker[Session], items: list[Item]) -> None:
    item_in = items[0]

    repo = SQLiteItemRepository(session=session_local)
    item = repo.get(obj_id=item_in.id)

    assert item
    assert item.id == item_in.id
    assert item.name == item_in.name
    assert item.description == item_in.description


def test_get_by_name(session_local: sessionmaker[Session], items: list[Item]) -> None:
    item_in = items[0]

    repo = SQLiteItemRepository(session=session_local)
    item = repo.get_by_name(item_name=item_in.name)

    assert item
    assert item.id == item_in.id
    assert item.name == item_in.name
    assert item.description == item_in.description


def test_get_multi(session_local: sessionmaker[Session], items: list[Item]) -> None:
    repo = SQLiteItemRepository(session=session_local)
    db_items = repo.get_multi()

    assert db_items == items


def test_update(session_local: sessionmaker[Session], items: list[Item]) -> None:
    item_in = items[0]

    repo = SQLiteItemRepository(session=session_local)
    item_update = ItemUpdate(description="updated description")
    repo.update(obj=item_in, update_data=item_update)

    stmt = text("SELECT name, description FROM item WHERE id = :id")
    with session_local() as session:
        row = session.execute(stmt, {"id": item_in.id}).first()

    assert row
    assert row.name == item_in.name
    assert row.description == item_update.description


def test_delete(session_local: sessionmaker[Session], items: list[Item]) -> None:
    item_in = items[0]

    repo = SQLiteItemRepository(session=session_local)
    repo.delete(item_in)

    stmt = text("SELECT name, description FROM item WHERE id = :id")
    with session_local() as session:
        row = session.execute(stmt, {"id": item_in.id}).first()

    assert not row
