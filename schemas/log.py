from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class LogBase(BaseModel):
    action: str
    task_id: int
    user_id: int
    project_id: int


class LogCreate(LogBase):
    pass


class Log(LogBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
      return cls(
        id=obj.id,
        action=obj.action,
        task_id=obj.task_id,
        user_id=obj.user_id,
        project_id=obj.project_id,
        created_at=obj.created_at.isoformat(),
        updated_at=obj.updated_at.isoformat()
    )