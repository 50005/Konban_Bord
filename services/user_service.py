from sqlalchemy.orm import Session
from models.user import User
from models.project import Project


class UserService:

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, email: str, password: str) -> User:
        user = User(username=username, email=email, password=password)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> User:
        return self.session.query(User).filter(User.username == username).first()

    def get_all_users(self) -> list[User]:
        return self.session.query(User).all()

    def update_user(self, user_id: int, username: str = None, email: str = None, password: str = None) -> User:
        user = self.get_user_by_id(user_id)
        if user:
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.password = password
            self.session.commit()
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def add_user_to_project(self, user_id: int, project_id: int) -> User:
        user = self.get_user_by_id(user_id)
        project = self.session.query(Project).filter(Project.id == project_id).first()

        if user and project:
            user.projects.append(project)
            self.session.commit()
        return user

    def remove_user_from_project(self, user_id: int, project_id: int) -> User:
        user = self.get_user_by_id(user_id)
        project = self.session.query(Project).filter(Project.id == project_id).first()

        if user and project:
            user.projects.remove(project)
            self.session.commit()
        return user