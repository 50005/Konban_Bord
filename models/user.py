from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base
from models.base import project_user_association, task_user_association

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    projects = relationship("Project", secondary=project_user_association, back_populates="users")
    logs = relationship("Log", back_populates="user", cascade="all, delete-orphan")
    users = relationship("Task", secondary=task_user_association)

    def __repr__(self):
        return f"<User id={self.id}, username='{self.username}'>"