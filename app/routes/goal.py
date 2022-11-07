from flask import Blueprint, jsonify, make_response, request
from app.models.goal_model import Goal
from app import db

goal_bp = Blueprint('goal_bp', __name__, url_prefix='/goals')
