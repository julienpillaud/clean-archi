from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text

from app.entities.item import Item, ItemCreate, ItemUpdate
from app.repository.sql.items import SQLiteItemRepository


def insert(session: sessionmaker[Session], items: list[Item]) -> None:
    item_1, item_2 = items
    stmt = text(
        """
        INSERT INTO item
        VALUES
            (:id1, :name1, :description1),
            (:id2, :name2, :description2)
        """
    )
    session().execute(
        stmt,
        {
            "id1": item_1.id,
            "name1": item_1.name,
            "description1": item_1.description,
            "id2": item_2.id,
            "name2": item_2.name,
            "description2": item_2.description,
        },
    )


def test_create(session: sessionmaker[Session]) -> None:
    repo = SQLiteItemRepository(session=session)
    item_create = ItemCreate(name="Item test", description="item test")
    repo.create(create_data=item_create)

    stmt = text("SELECT * FROM item WHERE name = :name")
    row = session().execute(stmt, {"name": item_create.name}).first()

    assert row
    assert row.name == item_create.name
    assert row.description == item_create.description


def test_get(session: sessionmaker[Session], items: list[Item]) -> None:
    item_in = items[0]
    insert(session, items)

    repo = SQLiteItemRepository(session=session)
    item = repo.get(obj_id=item_in.id)

    assert item
    assert item.id == item_in.id
    assert item.name == item_in.name
    assert item.description == item_in.description


def test_get_by_name(session: sessionmaker[Session], items: list[Item]) -> None:
    item_in = items[0]
    insert(session, items)

    repo = SQLiteItemRepository(session=session)
    item = repo.get_by_name(item_name=item_in.name)

    assert item
    assert item.id == item_in.id
    assert item.name == item_in.name
    assert item.description == item_in.description


def test_get_multi(session: sessionmaker[Session], items: list[Item]) -> None:
    insert(session, items)

    repo = SQLiteItemRepository(session=session)
    items = repo.get_multi()

    assert len(items) == 2


def test_update(session: sessionmaker[Session], items: list[Item]) -> None:
    item_in = items[0]
    insert(session, items)

    repo = SQLiteItemRepository(session=session)
    item_update = ItemUpdate(description="updated description")
    repo.update(obj=item_in, update_data=item_update)

    stmt = text("SELECT name, description FROM item WHERE id = :id")
    row = session().execute(stmt, {"id": item_in.id}).first()

    assert row
    assert row.name == item_in.name
    assert row.description == item_update.description


def test_delete(session: sessionmaker[Session], items: list[Item]) -> None:
    item_in = items[0]
    insert(session, items)

    repo = SQLiteItemRepository(session=session)
    repo.delete(item_in)

    stmt = text("SELECT name, description FROM item WHERE id = :id")
    row = session().execute(stmt, {"id": item_in.id}).first()

    assert not row
