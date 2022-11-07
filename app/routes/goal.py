from flask import Blueprint, abort, jsonify, make_response, request
from app.models.goal_model import Goal
from .helper import get_by_id
from app import db

goal_bp = Blueprint('goal_bp', __name__, url_prefix='/goals')

# take a goal and return it as a dictionary
def json_details(goal):
    return {
            "id": goal.goal_id,
            "title": goal.title,
            }

# return all goals as json
@goal_bp.route("", methods["GET"])
def get_goal():
    goals = Goal.query.all()
    response = [json_details(goal) for goal in goals]
    
    return jsonify(response), 200
    
# return one goal by id
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = get_by_id(Goal, goal_id)
    return json_details(goal), 200

# create a new goal
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()        
    
    try:
        new_goal = Goal(title = request_body["title"])
    except:
        return abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return json_details(new_goal), 201

# delete a goal by id
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = get_by_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"message": f"goal {goal.goal_id} successfully deleted"}, 200

# update a goal by id
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_task(goal_id):
    goal = get_by_id(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return json_details(goal), 200