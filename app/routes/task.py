from flask import Blueprint, jsonify, request
from app.models.task_model import Task
from datetime import datetime
from .helper import get_by_id
from app import db


task_bp = Blueprint('task_bp', __name__, url_prefix='/tasks')

# take a task and return it as a dictionary
def json_details(task):
    return {"task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        }

# return all tasks as json
@task_bp.route("", methods=["GET"])
def get_tasks():
    sort_query = request.args.get("sort")
    
    if sort_query:
        tasks = Task.query.order_by(Task.title.asc(), Task.title.desc())
        # tasks_asc = Task.query.order_by(Task.title.asc())
        # tasks_desc = Task.query.order_by(Task.title.desc())
        
        # if tasks_asc:
        #     tasks = tasks_asc
        # elif tasks_desc:
        #     tasks = tasks_desc
        
    else:
        tasks = Task.query.all()
        
    response = [{"id": task.task_id, "title": task.title, "description": task.description, "is_complete": bool(task.completed_at)} for task in tasks]
    return jsonify(response), 200
    
# return one task by id
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = get_by_id(Task, task_id)
        
    return json_details(task), 200

# return tasks by title
@task_bp.route("?title=<title>", methods=["GET"])

# create a new task
@task_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"])
        
        db.session.add(new_task)
        db.session.commit()

        return json_details(new_task), 201
    except Exception:
        return {
            "details": "Invalid data"
        }, 400

# delete a task by id
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_by_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200

# update a task by id
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = get_by_id(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return json_details(task), 200

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

    return json_details(task), 200
