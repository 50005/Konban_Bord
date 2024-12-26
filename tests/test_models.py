import unittest
from datetime import datetime
from models.base import Base
from models.project import Project
from models.task import Task
from models.user import User
from models.log import Log
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestModels(unittest.TestCase):

    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()

    def test_create_project(self):
        project = Project(title="Test Project")
        self.session.add(project)
        self.session.commit()
        self.assertIsNotNone(project.id)
        self.assertEqual(project.title, "Test Project")

    def test_create_column(self):
        project = Project(title="Test Project")
        self.session.add(project)
        self.session.commit()
        self.assertIsNotNone(project.id)

    def test_create_task(self):
        project = Project(title="Test Project")
        self.session.add(project)
        self.session.commit()
        task = Task(title="Test Task", project_id=project.id)
        self.session.add(task)
        self.session.commit()
        self.assertIsNotNone(task.id)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.project_id, project.id)

    def test_create_log(self):
        project = Project(title="Test Project")
        self.session.add(project)
        self.session.commit()

        task = Task(title="Test Task", project_id=project.id)
        self.session.add(task)
        self.session.commit()

        user = User(username="testuser", email="test@example.com", password="password")
        self.session.add(user)
        self.session.commit()

        log = Log(timestamp=datetime.utcnow(), action="Task created", task_id=task.id, user_id=user.id,
                  project_id=project.id)
        self.session.add(log)
        self.session.commit()
        self.assertIsNotNone(log.id)
        self.assertEqual(log.action, "Task created")

    def test_create_user(self):
        user = User(username="testuser", email="test@example.com", password="password")
        self.session.add(user)
        self.session.commit()
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "testuser")


if __name__ == '__main__':
    unittest.main()