from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..app import db
import requests

question_bp = Blueprint("question", __name__)


@question_bp.route("/<exam_id>", methods=["GET"])
@jwt_required()
def get_questions(exam_id):
    """Fetch questions from AQG and store in cloud."""
    aqg_response = requests.get(
        "https://aqg-service/api/generate", params={"exam_id": exam_id, "count": 10}
    )
    if aqg_response.status_code != 200:
        return jsonify({"error": "Failed to fetch from AQG"}), 500
    questions = aqg_response.json().get("questions", [])
    db.collection("questions").document(exam_id).set({"questions": questions})
    return jsonify(questions), 200
