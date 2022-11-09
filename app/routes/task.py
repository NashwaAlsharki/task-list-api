from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request
import requests

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"]
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        return {
            "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": bool(new_task.completed_at)
            }
        }, 201
    except Exception:
        return {
            "details": "Invalid data"
        }, 400

@task_bp.route("", methods=["GET"])
def get_tasks():
    
    sort_query = request.args.get("sort")
    
    if sort_query:
        tasks_asc = Task.query.order_by(Task.title.asc())
        tasks_desc = Task.query.order_by(Task.title.desc())
        
        if tasks_asc:
            task_response = [{"id": task.task_id, "title": task.title, "description": task.description, "is_complete": bool(task.completed_at)} for task in tasks_asc]

        elif tasks_desc:
            tasks = tasks_desc
            task_response = [{"id": task.task_id, "title": task.title, "description": task.description, "is_complete": bool(task.completed_at)} for task in tasks_desc]
        
    else:
        tasks = Task.query.all()

        task_response = [{"id": task.task_id, "title": task.title, "description": task.description, "is_complete": bool(task.completed_at)} for task in tasks]
            
    return jsonify(task_response), 200
    

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return {
            "message":"Task not found"
        }, 404
    
    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return {
            "message":"Task not found"
        }, 404
    
    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }, 200
    

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return {
            "message":"Task not found"
        }, 404
        
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }, 200