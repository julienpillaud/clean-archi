import uuid
from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.entities.item import Item
from app.repository.models import base

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session() -> Iterator[sessionmaker[Session]]:
    base.Base.metadata.create_all(bind=engine)
    yield SessionLocal
    base.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def items() -> list[Item]:
    item_id_1 = str(uuid.uuid4())
    item_id_2 = str(uuid.uuid4())
    return [
        Item(id=item_id_1, name="Item1", description="item 1"),
        Item(id=item_id_2, name="Item2", description="item 2"),
    ]
