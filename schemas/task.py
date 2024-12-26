from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    project_id: int
    column_id: int
    user_id: int
    description: Optional[str] = None
    status: str


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
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
        project_id=obj.project_id,
        column_id=obj.column_id,
        user_id=obj.user_id,
        description=obj.description,
        status=obj.status,
        created_at=obj.created_at.isoformat(),
        updated_at=obj.updated_at.isoformat()
    )