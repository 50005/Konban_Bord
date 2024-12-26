import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from services.column_service import ColumnService


class TestColumnService(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.column_service = ColumnService(self.session)

    def tearDown(self):
        self.session.close()

    def test_create_column(self):
        column = self.column_service.create_column(title="Test Column")
        self.assertIsNotNone(column.id)
        self.assertEqual(column.title, "Test Column")

    def test_get_column_by_id(self):
        column = self.column_service.create_column(title="Test Column")
        retrieved_column = self.column_service.get_column_by_id(column.id)
        self.assertEqual(column.id, retrieved_column.id)
        self.assertEqual(column.title, retrieved_column.title)

    def test_get_all_columns(self):
        self.column_service.create_column(title="Test Column 1")
        self.column_service.create_column(title="Test Column 2")
        columns = self.column_service.get_all_columns()
        self.assertEqual(len(columns), 2)

    def test_update_column(self):
        column = self.column_service.create_column(title="Test Column")
        updated_column = self.column_service.update_column(column.id, title="Updated Column")
        self.assertEqual(updated_column.title, "Updated Column")

    def test_delete_column(self):
        column = self.column_service.create_column(title="Test Column")
        is_deleted = self.column_service.delete_column(column.id)
        self.assertTrue(is_deleted)
        deleted_column = self.column_service.get_column_by_id(column.id)
        self.assertIsNone(deleted_column)


if __name__ == '__main__':
    unittest.main()