# routes/column_routes.py
from flask import Blueprint, request, jsonify, render_template
from sqlalchemy.orm import Session
from services.column_service import ColumnService
from database import get_db
from models.column import Column  # Импорт модели Column из models

column_blueprint = Blueprint('column', __name__)

@column_blueprint.route("/", methods=["POST"])
def create_column():
    column = ColumnCreate(**request.form)
    db: Session = next(get_db())
    column_service = ColumnService(db)
    created_column = column_service.create_column(title=column.title)
    return render_template("column/view.html", column=Column.from_orm(created_column)), 201

@column_blueprint.route("/create", methods=["GET"])
def create_column_form():
    return render_template("column/create.html")

@column_blueprint.route("/<int:column_id>", methods=["GET"])
def get_column_by_id(column_id: int):
    db: Session = next(get_db())
    column_service = ColumnService(db)
    column = column_service.get_column_by_id(column_id)
    if not column:
        return jsonify({"message": "Column not found"}), 404
    return render_template("column/view.html", column=Column.from_orm(column))

@column_blueprint.route("/", methods=["GET"])
def get_all_columns():
    db: Session = next(get_db())
    column_service = ColumnService(db)
    columns = column_service.get_all_columns()
    return render_template("column/view_all.html", columns=[Column.from_orm(column) for column in columns])

@column_blueprint.route("/<int:column_id>/edit", methods=["GET"])
def get_edit_column_form(column_id: int):
    db: Session = next(get_db())
    column_service = ColumnService(db)
    column = column_service.get_column_by_id(column_id)
    if not column:
        return jsonify({"message": "Column not found"}), 404
    return render_template("column/edit.html", column=Column.from_orm(column))

@column_blueprint.route("/<int:column_id>", methods=["POST"])
def update_column(column_id: int):
    column = ColumnUpdate(**request.form)
    db: Session = next(get_db())
    column_service = ColumnService(db)
    updated_column = column_service.update_column(column_id=column_id, title=column.title)
    if not updated_column:
        return jsonify({"message": "Column not found"}), 404
    return render_template("column/view.html", column=Column.from_orm(updated_column))

@column_blueprint.route("/<int:column_id>/delete", methods=["GET"])
def get_delete_column_form(column_id: int):
    db: Session = next(get_db())
    column_service = ColumnService(db)
    column = column_service.get_column_by_id(column_id)
    if not column:
        return jsonify({"message": "Column not found"}), 404
    return render_template("column/delete.html", column=Column.from_orm(column))

@column_blueprint.route("/<int:column_id>", methods=["DELETE"])
def delete_column(column_id: int):
    db: Session = next(get_db())
    column_service = ColumnService(db)
    if not column_service.delete_column(column_id):
        return jsonify({"message": "Column not found"}), 404
    return render_template("column/view.html")