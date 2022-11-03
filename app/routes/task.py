from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

task_bp = Blueprint('task_bp', __name__, url_prefix='/tasks')

@task_bp.route("", methods=["GET"])
def get_tasks():

    tasks = Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        })
    
    if not task_response:
        return task_response, 200
    return jsonify(task_response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    
    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
    }, 200

@task_bp.route("/<title>", methods=["GET"])

@task_bp.route("/<completed_at>", methods=["GET"])

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    
    db.session.delete(task)
    db.session.commit()

    return {
        "message": f"Task {task.task_id} successfully deleted"
    }, 200
    

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
        
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
    }, 200


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

    return make_response(f"Task {new_task.title} has been successfully created!", 201)

