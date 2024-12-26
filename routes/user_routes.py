from flask import Blueprint, request, jsonify, render_template
from sqlalchemy.orm import Session
from services.user_service import UserService
from database import get_db
from schemas.user import UserCreate, UserUpdate, User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route("/", methods=["POST"])
def create_user():
    user = UserCreate(**request.form)
    db: Session = next(get_db())
    user_service = UserService(db)
    created_user = user_service.create_user(
        username=user.username,
        email=user.email,
        password=user.password
    )
    return render_template("user/view.html", user=User.from_orm(created_user)), 201

@user_blueprint.route("/create", methods=["GET"])
def create_user_form():
    return render_template("user/create.html")

@user_blueprint.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int):
    db: Session = next(get_db())
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return render_template("user/view.html", user=User.from_orm(user))

@user_blueprint.route("/", methods=["GET"])
def get_all_users():
    db: Session = next(get_db())
    user_service = UserService(db)
    users = user_service.get_all_users()
    return render_template("user/view_all.html", users=[User.from_orm(user) for user in users])

@user_blueprint.route("/<int:user_id>/edit", methods=["GET"])
def get_edit_user_form(user_id: int):
    db: Session = next(get_db())
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return render_template("user/edit.html", user=User.from_orm(user))

@user_blueprint.route("/<int:user_id>", methods=["POST"])
def update_user(user_id: int):
    user = UserUpdate(**request.form)
    db: Session = next(get_db())
    user_service = UserService(db)
    updated_user = user_service.update_user(
        user_id=user_id,
        username=user.username,
        email=user.email,
    )
    if not updated_user:
        return jsonify({"message": "User not found"}), 404
    return render_template("user/view.html", user=User.from_orm(updated_user))

@user_blueprint.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    db: Session = next(get_db())
    user_service = UserService(db)
    if not user_service.delete_user(user_id):
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200