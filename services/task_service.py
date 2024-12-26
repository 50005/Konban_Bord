from sqlalchemy.orm import Session
from models.task import Task
from sqlalchemy import or_
from services.log_service import LogService
from datetime import datetime
from models.log import Log


class TaskService:

    def __init__(self, session: Session):
        self.session = session
        self.log_service = LogService(session)

    def create_task(self, title: str, project_id: int, column_id: int, user_id: int, description: str = None,
                    status: str = "В очереди") -> Task:
        task = Task(title=title, description=description, project_id=project_id, column_id=column_id, status=status)
        self.session.add(task)
        self.session.commit()
        print(f"Task created: id={task.id}, title={task.title}")

        self.log_service.create_log(action="Task created", task_id=task.id, user_id=user_id, project_id=project_id)
        return task

    def get_task_by_id(self, task_id: int) -> Task:
        task = self.session.query(Task).filter(Task.id == task_id).first()
        print(f"Task retrieved: id={task_id}, task={task}")
        return task

    def get_all_tasks(self) -> list[Task]:
        tasks = self.session.query(Task).all()
        print(f"All tasks retrieved: {tasks}")
        return tasks

    def update_task(self, task_id: int, user_id: int, title: str = None, description: str = None, status: str = None,
                    column_id: int = None) -> Task:
        task = self.get_task_by_id(task_id)
        if task:
            log_message = []
            if title and task.title != title:
                log_message.append(f"Title changed from '{task.title}' to '{title}'")
                task.title = title
            if description and task.description != description:
                log_message.append(f"Description changed from '{task.description}' to '{description}'")
                task.description = description
            if status and task.status != status:
                log_message.append(f"Status changed from '{task.status}' to '{status}'")
                task.status = status
            if column_id and task.column_id != column_id:
                log_message.append(f"Column id changed from '{task.column_id}' to '{column_id}'")
                task.column_id = column_id

            if log_message:
                self.log_service.create_log(action=', '.join(log_message), task_id=task.id, user_id=user_id,
                                            project_id=task.project_id)
            self.session.commit()
            print(
                f"Task updated: id={task.id}, title={task.title}, description={task.description}, status={task.status}, column_id={task.column_id}")

        return task

    def delete_task(self, task_id: int, user_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            print(f"Deleting task: id={task.id}, title={task.title}")
            self.log_service.create_log(action="Task deleted", task_id=task.id, user_id=user_id,
                                        project_id=task.project_id)
            self.session.delete(task)  # remove comment
            self.session.commit()
            print(f"Task deleted: id={task_id}")
            return True
        return False

    def get_tasks_by_column(self, column_id: int, filter_params: dict = None) -> list[Task]:
        query = self.session.query(Task).filter(Task.column_id == column_id)

        if filter_params:
            filters = []
            for key, value in filter_params.items():
                if hasattr(Task, key):
                    filters.append(getattr(Task, key).like(f"%{value}%"))
            if filters:
                query = query.filter(or_(*filters))
        tasks = query.all()
        print(f"Tasks by column: column_id={column_id}, filter_params={filter_params}, tasks={tasks}")
        return tasks

    def task_log(self, task_id: int):
        logs = self.session.query(Log).filter(Log.task_id == task_id).all()
        print(f"Task id in task_log: {task_id}")
        print(f"Logs in task_log: {logs}")
        return logs