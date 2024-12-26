from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str

class UserAddToProject(BaseModel):
   user_id: int
   project_id: int

class UserRemoveFromProject(BaseModel):
   user_id: int
   project_id: int

class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: str
    updated_at: str
    projects: Optional[List[int]] = None

    class Config:
        from_attributes = True
    @classmethod
    def from_orm(cls, obj):
      return cls(
        id=obj.id,
        username=obj.username,
        email=obj.email,
        created_at=obj.created_at.isoformat(),
        updated_at=obj.updated_at.isoformat(),
         projects = [project.id for project in obj.projects] if obj.projects else None
    )