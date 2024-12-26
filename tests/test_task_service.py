import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from services.project_service import ProjectService
from services.task_service import TaskService
from services.column_service import ColumnService
from services.user_service import UserService
from models.log import Log


class TestTaskService(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.task_service = TaskService(self.session)
        self.project_service = ProjectService(self.session)
        self.column_service = ColumnService(self.session)
        self.user_service = UserService(self.session)
        self.project = self.project_service.create_project(title="Test Project")
        self.column = self.column_service.create_column(title="Test Column")
        self.user = self.user_service.create_user(username="testuser", email="test@test.com", password="password")

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_create_task(self):
        task = self.task_service.create_task(title="Test Task", project_id=self.project.id, column_id=self.column.id,
                                             user_id=self.user.id, description="Test Description")
        self.assertIsNotNone(task.id)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")

    def test_get_task_by_id(self):
        task = self.task_service.create_task(title="Test Task", project_id=self.project.id, column_id=self.column.id,
                                             user_id=self.user.id)
        retrieved_task = self.task_service.get_task_by_id(task.id)
        self.assertEqual(task.id, retrieved_task.id)
        self.assertEqual(task.title, retrieved_task.title)

    def test_get_all_tasks(self):
        self.task_service.create_task(title="Test Task 1", project_id=self.project.id, column_id=self.column.id,
                                      user_id=self.user.id)
        self.task_service.create_task(title="Test Task 2", project_id=self.project.id, column_id=self.column.id,
                                      user_id=self.user.id)
        tasks = self.task_service.get_all_tasks()
        self.assertEqual(len(tasks), 2)

    def test_update_task(self):
        task = self.task_service.create_task(title="Test Task", project_id=self.project.id, column_id=self.column.id,
                                             user_id=self.user.id)
        updated_task = self.task_service.update_task(task.id, user_id=self.user.id, title="Updated Task",
                                                     description="Updated Description", status="В работе")
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertEqual(updated_task.description, "Updated Description")
        self.assertEqual(updated_task.status, "В работе")

    def test_delete_task(self):
        task = self.task_service.create_task(title="Test Task", project_id=self.project.id, column_id=self.column.id,
                                             user_id=self.user.id)
        is_deleted = self.task_service.delete_task(task.id, user_id=self.user.id)
        self.assertTrue(is_deleted)
        deleted_task = self.task_service.get_task_by_id(task.id)
        self.assertIsNone(deleted_task)

    def test_get_tasks_by_column(self):
        task1 = self.task_service.create_task(title="Test Task 1", project_id=self.project.id, column_id=self.column.id,
                                              user_id=self.user.id)
        task2 = self.task_service.create_task(title="Test Task 2", project_id=self.project.id, column_id=self.column.id,
                                              user_id=self.user.id, status="В работе")
        tasks = self.task_service.get_tasks_by_column(self.column.id)
        self.assertEqual(len(tasks), 2)

    def test_get_tasks_by_column_with_filter(self):
        task1 = self.task_service.create_task(title="Test Task 1", project_id=self.project.id, column_id=self.column.id,
                                              user_id=self.user.id)
        task2 = self.task_service.create_task(title="Test Task 2", project_id=self.project.id, column_id=self.column.id,
                                              user_id=self.user.id, status="В работе")
        tasks = self.task_service.get_tasks_by_column(self.column.id, filter_params={"title": "Task 1"})
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, task1.id)

    def test_task_log(self):
        task = self.task_service.create_task(title="Test Task", project_id=self.project.id, column_id=self.column.id,
                                             user_id=self.user.id)

        # Проверка лога создания
        logs_after_creation = self.session.query(Log).filter(Log.task_id == task.id).all()

        # Проверка лога обновления
        self.task_service.update_task(task.id, user_id=self.user.id, title="Updated Task",
                                      description="Updated Description", status="В работе")
        logs_after_update = self.session.query(Log).filter(Log.task_id == task.id).all()

        # Проверка лога удаления
        logs_before_delete = self.session.query(Log).filter(Log.task_id == task.id).all()
        self.task_service.delete_task(task.id, user_id=self.user.id)
        logs_after_delete = self.session.query(Log).filter(Log.task_id == task.id).all()