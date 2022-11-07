from flask import Blueprint, jsonify, request
from app.models.task_model import Task
from datetime import datetime
from .helper import get_by_id, json_details, get_all
from app import db


task_bp = Blueprint('task_bp', __name__, url_prefix='/tasks')

# return all tasks as json
@task_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    response = [json_details(Task, task) for task in tasks]
    
    return jsonify(response), 200
    
# return one task by id
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = get_by_id(Task, task_id)
    return json_details(Task, task), 200

# return tasks by title
@task_bp.route("?title=<title>", methods=["GET"])

# create a new task
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"])
    
    db.session.add(new_task)
    db.session.commit()

    return json_details(Task, new_task), 201

# delete a task by id
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_by_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"message": f"Task {task.task_id} successfully deleted"}, 200

# update a task by id
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = get_by_id(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return json_details(Task, task), 200

# return task complete/incomplete status
@task_bp.route("/<task_id>/<complete>", methods=["PATCH"])
def task_complete_status(complete, task_id):
    task = get_by_id(Task, task_id)

    if complete == "mark_complete":
        if not task.completed_at:
            task.completed_at = datetime.now()

    elif complete == "mark_incomplete":
        task.completed_at = None
    
    db.session.commit()

    return json_details(Task, task), 200
