import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from services.user_service import UserService
from services.project_service import ProjectService


class TestUserService(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.user_service = UserService(self.session)
        self.project_service = ProjectService(self.session)
        self.project = self.project_service.create_project(title="Test Project")

    def tearDown(self):
        self.session.close()

    def test_create_user(self):
        user = self.user_service.create_user(username="testuser", email="test@test.com", password="password")
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@test.com")

    def test_get_user_by_id(self):
        user = self.user_service.create_user(username="testuser", email="test@test.com", password="password")
        retrieved_user = self.user_service.get_user_by_id(user.id)
        self.assertEqual(user.id, retrieved_user.id)
        self.assertEqual(user.username, retrieved_user.username)

    def test_get_user_by_username(self):
        user = self.user_service.create_user(username="testuser", email="test@test.com", password="password")
        retrieved_user = self.user_service.get_user_by_username(user.username)
        self.assertEqual(user.id, retrieved_user.id)
        self.assertEqual(user.username, retrieved_user.username)

    def test_get_all_users(self):
        self.user_service.create_user(username="testuser1", email="test1@test.com", password="password")
        self.user_service.create_user(username="testuser2", email="test2@test.com", password="password")
        users = self.user_service.get_all_users()
        self.assertEqual(len(users), 2)

    def test_update_user(self):
        user = self.user_service.create_user(username="testuser", email="test@test.com", password="password")
        updated_user = self.user_service.update_user(user.id, username="updateduser", email="updated@test.com",
                                                     password="newpassword")
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.email, "updated@test.com")
        self.assertEqual(updated_user.password, "newpassword")

    def test_delete_user(self):
        user = self.user_service.create_user(username="testuser", email="test@test.com", password="password")
        is_deleted = self.user_service.delete_user(user.id)
        self.assertTrue(is_deleted)
        deleted_user = self.user_service.get_user_by_id(user.id)
        self.assertIsNone(deleted_user)

    def test_add_user_to_project(self):
        user = self.user_service.create_user(username="testuser", email="test@test.com", password="password")
        user_get = self.user_service.add_user_to_project(user.id, self.project.id)
        self.assertEqual(len(user_get.projects), 1)

    def test_remove_user_from_project(self):
        user = self.user_service.create_user(username="testuser", email="test@test.com", password="password")
        self.user_service.add_user_to_project(user.id, self.project.id)
        user_get = self.user_service.remove_user_from_project(user.id, self.project.id)
        self.assertEqual(len(user_get.projects), 0)


if __name__ == '__main__':
    unittest.main()