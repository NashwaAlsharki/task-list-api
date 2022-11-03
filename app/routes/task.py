from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

task_bp = Blueprint('task_bp', __name__, url_prefix='/tasks')

""" @task_bp.route("", methods=["GET"])
def all_tasks():
@task_bp.route("/<task_id>", methods=["GET"])
@task_bp.route("/<title>", methods=["GET"])
@task_bp.route("/<completed_at>", methods=["GET"])
@task_bp.route("/<task_id>", methods=["DELETE"])
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id): """

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )
    
    db.session.add(new_task)
    db.session.commit()

    # Successful response
    return make_response(f"Task {new_task.title} has been successfully created!", 201)

