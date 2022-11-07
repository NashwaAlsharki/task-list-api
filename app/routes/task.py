from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

task_bp = Blueprint('task_bp', __name__, url_prefix='/tasks')

def validate_id(id):
    try:
        int(id)
    except ValueError:
        return make_response("", 404)
    
    task = Task.query.get(id)
    return task

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
    
    task = validate_id(task_id)
    
    return {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
            }, 200

@task_bp.route("/<title>", methods=["GET"])
def get_one_task_by_title(title):
        
        task = Task.query.filter_by(title=title).first()
        
        return {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete
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

    return {f"Task {new_task.title} has been successfully created!"}, 201

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    
    task = validate_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"message": f"Task {task.task_id} successfully deleted"}, 200
    

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    
    task = validate_id(task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
            }, 200

@app.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_task(client, task_id):
        
        task = validate_id(task_id)

        if not task.completed_at:
            task.completed_at = datetime.utcnow()
            db.session.commit()
    
        return {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": True
                }, 200

@app.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_task(client, task_id):
            
            task = validate_id(task_id)
    
            if task.completed_at:
                task.completed_at = None
                db.session.commit()
        
            return {
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": False
                    }, 200
