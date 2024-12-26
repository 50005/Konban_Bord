from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String, nullable=False)
    task_id = Column(Integer, ForeignKey('task.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    project_id = Column(Integer, ForeignKey('project.id'))

    task = relationship("Task", back_populates="logs")
    user = relationship("User", back_populates="logs")
    project = relationship("Project", back_populates="logs")

    def __repr__(self):
        return f"<Log id={self.id}, action='{self.action}'>"