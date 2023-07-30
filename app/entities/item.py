from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


class ItemBase(BaseModel):
    name: str | None = None
    description: str | None = None

    @model_validator(mode="before")
    @classmethod
    def any_of(cls, data: Any) -> Any:
        if isinstance(data, dict):
            assert (
                "name" in data or "description" in data
            ), "At least one filed is required"
        return data


class ItemCreate(ItemBase):
    name: str


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str
