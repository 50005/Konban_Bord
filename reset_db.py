from database import Base, engine

# Удаление всех таблиц
Base.metadata.drop_all(engine)

# Создание всех таблиц
Base.metadata.create_all(engine)

print("Database has been reset.")