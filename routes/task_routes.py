# routes/task_routes.py
from flask import Blueprint, request, jsonify, render_template
from sqlalchemy.orm import Session
from services.task_service import TaskService
from database import get_db
from models.task import Task  # Измените импорт для использования модели из models

task_blueprint = Blueprint('task', __name__)

@task_blueprint.route("/", methods=["POST"])
def create_task():
    task = TaskCreate(**request.form)
    db: Session = next(get_db())
    task_service = TaskService(db)
    created_task = task_service.create_task(
        title=task.title,
        project_id=task.project_id,
        column_id=task.column_id,
        user_id=task.user_id,
        description=task.description,
        status=task.status
    )
    return render_template("task/view.html", task=Task.from_orm(created_task)), 201

@task_blueprint.route("/create", methods=["GET"])
def create_task_form():
    return render_template("task/create.html")

@task_blueprint.route("/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id: int):
    db: Session = next(get_db())
    task_service = TaskService(db)
    task = task_service.get_task_by_id(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    return render_template("task/view.html", task=Task.from_orm(task))

@task_blueprint.route("/", methods=["GET"])
def get_all_tasks():
    db: Session = next(get_db())
    task_service = TaskService(db)
    tasks = task_service.get_all_tasks()
    return render_template("task/view_all.html", tasks=[Task.from_orm(task) for task in tasks])

@task_blueprint.route("/column/<int:column_id>", methods=["GET"])
def get_tasks_by_column(column_id: int):
    db: Session = next(get_db())
    task_service = TaskService(db)
    tasks = task_service.get_tasks_by_column(column_id)
    return render_template("task/view_all.html", tasks=[Task.from_orm(task) for task in tasks])

@task_blueprint.route("/<int:task_id>/edit", methods=["GET"])
def get_edit_task_form(task_id: int):
    db: Session = next(get_db())
    task_service = TaskService(db)
    task = task_service.get_task_by_id(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    return render_template("task/edit.html", task=Task.from_orm(task))

@task_blueprint.route("/<int:task_id>", methods=["POST"])
def update_task(task_id: int):
    task = TaskUpdate(**request.form)
    db: Session = next(get_db())
    task_service = TaskService(db)
    updated_task = task_service.update_task(
        task_id=task_id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        status=task.status,
        column_id=task.column_id
    )
    if not updated_task:
        return jsonify({"message": "Task not found"}), 404
    return render_template("task/view.html", task=Task.from_orm(updated_task))

@task_blueprint.route("/<int:task_id>/delete", methods=["GET"])
def get_delete_task_form(task_id: int):
    db: Session = next(get_db())
    task_service = TaskService(db)
    task = task_service.get_task_by_id(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    return render_template("task/delete.html", task=Task.from_orm(task))

@task_blueprint.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    db: Session = next(get_db())
    task_service = TaskService(db)
    if not task_service.delete_task(task_id):
        return jsonify({"message": "Task not found"}), 404
    return render_template("task/view.html")