from flask import Blueprint, request, jsonify, render_template
from sqlalchemy.orm import Session
from services.project_service import ProjectService
from database import get_db
from schemas.project import ProjectCreate, ProjectUpdate, Project

project_blueprint = Blueprint('project', __name__)

@project_blueprint.route("/", methods=["POST"])
def create_project():
    project = ProjectCreate(**request.form)
    db: Session = next(get_db())
    project_service = ProjectService(db)
    created_project = project_service.create_project(title=project.title)
    return render_template("project/view.html", project=Project.from_orm(created_project)), 201

@project_blueprint.route("/create", methods=["GET"])
def create_project_form():
    return render_template("project/create.html")

@project_blueprint.route("/<int:project_id>", methods=["GET"])
def get_project_by_id(project_id: int):
    db: Session = next(get_db())
    project_service = ProjectService(db)
    project = project_service.get_project_by_id(project_id)
    if not project:
        return jsonify({"message": "Project not found"}), 404
    return render_template("project/view.html", project=Project.from_orm(project))

@project_blueprint.route("/", methods=["GET"])
def get_all_projects():
    db: Session = next(get_db())
    project_service = ProjectService(db)
    projects = project_service.get_all_projects()
    return render_template("project/view_all.html", projects=[Project.from_orm(project) for project in projects])

@project_blueprint.route("/<int:project_id>/edit", methods=["GET"])
def get_edit_project_form(project_id: int):
    db: Session = next(get_db())
    project_service = ProjectService(db)
    project = project_service.get_project_by_id(project_id)
    if not project:
        return jsonify({"message": "Project not found"}), 404
    return render_template("project/edit.html", project=Project.from_orm(project))

@project_blueprint.route("/<int:project_id>", methods=["POST"])
def update_project(project_id: int):
    project = ProjectUpdate(**request.form)
    db: Session = next(get_db())
    project_service = ProjectService(db)
    updated_project = project_service.update_project(project_id=project_id, title=project.title)
    if not updated_project:
        return jsonify({"message": "Project not found"}), 404
    return render_template("project/view.html", project=Project.from_orm(updated_project))

@project_blueprint.route("/<int:project_id>/delete", methods=["GET"])
def get_delete_project_form(project_id: int):
    db: Session = next(get_db())
    project_service = ProjectService(db)
    project = project_service.get_project_by_id(project_id)
    if not project:
        return jsonify({"message": "Project not found"}), 404
    return render_template("project/delete.html", project=Project.from_orm(project))

@project_blueprint.route("/<int:project_id>", methods=["DELETE"])
def delete_project(project_id: int):
    db: Session = next(get_db())
    project_service = ProjectService(db)
    if not project_service.delete_project(project_id):
        return jsonify({"message": "Project not found"}), 404
    return render_template("project/view.html")