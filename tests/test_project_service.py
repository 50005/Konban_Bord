import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from services.project_service import ProjectService


class TestProjectService(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.project_service = ProjectService(self.session)

    def tearDown(self):
        self.session.close()

    def test_create_project(self):
        project = self.project_service.create_project(title="Test Project", description="Test Description")
        self.assertIsNotNone(project.id)
        self.assertEqual(project.title, "Test Project")
        self.assertEqual(project.description, "Test Description")

    def test_get_project_by_id(self):
        project = self.project_service.create_project(title="Test Project")
        retrieved_project = self.project_service.get_project_by_id(project.id)
        self.assertEqual(project.id, retrieved_project.id)
        self.assertEqual(project.title, retrieved_project.title)

    def test_get_all_projects(self):
        self.project_service.create_project(title="Test Project 1")
        self.project_service.create_project(title="Test Project 2")
        projects = self.project_service.get_all_projects()
        self.assertEqual(len(projects), 2)

    def test_update_project(self):
        project = self.project_service.create_project(title="Test Project")
        updated_project = self.project_service.update_project(project.id, title="Updated Project",
                                                              description="Updated Description")
        self.assertEqual(updated_project.title, "Updated Project")
        self.assertEqual(updated_project.description, "Updated Description")

    def test_delete_project(self):
        project = self.project_service.create_project(title="Test Project")
        is_deleted = self.project_service.delete_project(project.id)
        self.assertTrue(is_deleted)
        deleted_project = self.project_service.get_project_by_id(project.id)
        self.assertIsNone(deleted_project)


if __name__ == '__main__':
    unittest.main()