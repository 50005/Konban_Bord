# create_tables.py
from database import Base, engine
from models.task import Task
from models.column import Column
from models.project import Project

# Пересоздайте все таблицы в правильном порядке
print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)
print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Tables have been recreated successfully.")