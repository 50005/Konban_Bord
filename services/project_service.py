from sqlalchemy.orm import Session
from models.project import Project

class ProjectService:

    def __init__(self, session: Session):
        self.session = session

    def create_project(self, title: str, description: str = None) -> Project:
        project = Project(title=title, description=description)
        self.session.add(project)
        self.session.commit()
        return project

    def get_project_by_id(self, project_id: int) -> Project:
        return self.session.query(Project).filter(Project.id == project_id).first()

    def get_all_projects(self) -> list[Project]:
        return self.session.query(Project).all()

    def update_project(self, project_id: int, title: str = None, description: str = None) -> Project:
        project = self.get_project_by_id(project_id)
        if project:
            if title:
                project.title = title
            if description:
                project.description = description
            self.session.commit()
        return project

    def delete_project(self, project_id: int) -> bool:
        project = self.get_project_by_id(project_id)
        if project:
            self.session.delete(project)
            self.session.commit()
            return True
        return False