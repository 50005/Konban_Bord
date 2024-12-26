from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ColumnBase(BaseModel):
    title: str


class ColumnCreate(ColumnBase):
    pass


class ColumnUpdate(ColumnBase):
    pass


class ColumnModel(ColumnBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            title=obj.title,
            created_at=obj.created_at.isoformat(),
            updated_at=obj.updated_at.isoformat()
        )