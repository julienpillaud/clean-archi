import uuid
from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.entities.item import Item
from app.repository.models import base

engine = create_engine("postgresql://test:test@localhost:5432/test")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session_local() -> Iterator[sessionmaker[Session]]:
    base.Base.metadata.create_all(bind=engine)
    yield SessionLocal
    base.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def items(session_local: sessionmaker[Session]) -> list[Item]:
    item_id_1 = str(uuid.uuid4())
    item_id_2 = str(uuid.uuid4())
    item_1 = Item(id=item_id_1, name="Item1", description="item 1")
    item_2 = Item(id=item_id_2, name="Item2", description="item 2")

    stmt = text(
        """
        INSERT INTO item
        VALUES
            (:id1, :name1, :description1),
            (:id2, :name2, :description2)
        """
    )
    with session_local() as session:
        session.execute(
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
        session.commit()

    return [item_1, item_2]
