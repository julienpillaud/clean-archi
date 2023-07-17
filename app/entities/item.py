from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    name: str | None = None
    description: str | None = None


class ItemCreate(ItemBase):
    name: str


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str
