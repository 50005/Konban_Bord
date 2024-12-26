from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from services.log_service import LogService
from database import get_db
from schemas.log import LogCreate, Log

log_blueprint = Blueprint('log', __name__)


@log_blueprint.route("/", methods=["POST"])
def create_log():
    log = LogCreate(**request.get_json())
    db: Session = next(get_db())
    log_service = LogService(db)
    created_log = log_service.create_log(
        action=log.action,
        task_id=log.task_id,
        user_id=log.user_id,
        project_id=log.project_id
    )
    return jsonify(Log.from_orm(created_log).dict()), 201


@log_blueprint.route("/<int:log_id>", methods=["GET"])
def get_log_by_id(log_id: int):
    db: Session = next(get_db())
    log_service = LogService(db)
    log = log_service.get_log_by_id(log_id)
    if not log:
        return jsonify({"message": "Log not found"}), 404
    return jsonify(Log.from_orm(log).dict()), 200

@log_blueprint.route("/task/<int:task_id>", methods=["GET"])
def get_logs_by_task(task_id: int):
    db: Session = next(get_db())
    log_service = LogService(db)
    logs = log_service.get_logs_by_task(task_id)
    return jsonify([Log.from_orm(log).dict() for log in logs]), 200

@log_blueprint.route("/", methods=["GET"])
def get_all_logs():
    db: Session = next(get_db())
    log_service = LogService(db)
    logs = log_service.get_all_logs()
    return jsonify([Log.from_orm(log).dict() for log in logs]), 200


@log_blueprint.route("/<int:log_id>", methods=["DELETE"])
def delete_log(log_id: int):
    db: Session = next(get_db())
    log_service = LogService(db)
    if not log_service.delete_log(log_id):
        return jsonify({"message": "Log not found"}), 404
    return jsonify({"message": "Log deleted"}), 200