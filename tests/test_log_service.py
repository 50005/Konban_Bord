import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from services.log_service import LogService


class TestLogService(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.log_service = LogService(self.session)

    def tearDown(self):
        self.session.close()

    def test_create_log(self):
        log = self.log_service.create_log(action="Test Action", task_id=1, user_id=1, project_id=1)
        self.assertIsNotNone(log.id)
        self.assertEqual(log.action, "Test Action")

    def test_get_log_by_id(self):
        log = self.log_service.create_log(action="Test Action", task_id=1, user_id=1, project_id=1)
        retrieved_log = self.log_service.get_log_by_id(log.id)
        self.assertEqual(log.id, retrieved_log.id)
        self.assertEqual(retrieved_log.action, "Test Action")

    def test_get_all_logs(self):
        self.log_service.create_log(action="Test Action 1", task_id=1, user_id=1, project_id=1)
        self.log_service.create_log(action="Test Action 2", task_id=2, user_id=2, project_id=2)
        logs = self.log_service.get_all_logs()
        self.assertEqual(len(logs), 2)

    def test_delete_log(self):
        log = self.log_service.create_log(action="Test Action", task_id=1, user_id=1, project_id=1)
        is_deleted = self.log_service.delete_log(log.id)
        self.assertTrue(is_deleted)
        deleted_log = self.log_service.get_log_by_id(log.id)
        self.assertIsNone(deleted_log)