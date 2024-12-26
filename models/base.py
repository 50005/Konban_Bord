from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from datetime import datetime

# Создаем базовый класс для моделей
Base = declarative_base()

project_user_association = Table(
    "project_user_association",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True)
)

task_user_association = Table(
    "task_user_association",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("task.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
)

class ColumnModel(Base):
    __tablename__ = "column"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tasks = relationship("Task", back_populates="column")

if __name__ == '__main__':
    # Устанавливаем соединение с базой данных (SQLite в примере)
    engine = create_engine("sqlite:///./kanban.db", echo=True)

    # Создаем все таблицы, если их еще нет
    Base.metadata.create_all(engine)

    # Создаем сессию
    Session = sessionmaker(bind=engine)
    session = Session()

    # Выводим все таблицы в базе данных
    print("Tables in the database:")
    print(Base.metadata.tables)

    # Закрываем сессию
    session.close()