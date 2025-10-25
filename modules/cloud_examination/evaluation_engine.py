from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..app import db
import requests

evaluation_bp = Blueprint("evaluation", __name__)


@evaluation_bp.route("/<submission_id>", methods=["POST"])
@jwt_required()
def evaluate_submission(submission_id):
    """Auto-evaluate responses (MCQ auto, subjective AI/manual)."""
    submission = db.collection("submissions").document(submission_id).get()
    if not submission.exists:
        return jsonify({"error": "Submission not found"}), 404

    data = submission.to_dict()
    responses = data["responses"]
    questions_doc = db.collection("questions").document(data["exam_id"]).get()
    questions = questions_doc.to_dict().get("questions", [])

    score = 0
    for resp in responses:
        q = next((q for q in questions if q["id"] == resp["question_id"]), None)
        if q and q["type"] == "MCQ" and resp["answer"] == q["correct_answer"]:
            score += q["marks"]

    result = {
        "submission_id": submission_id,
        "score": score,
        "analytics": {"total_questions": len(questions)},
    }
    db.collection("results").document(submission_id).set(result)

    # Notify Progress Tracker
    requests.post("https://progress-tracker/api/update", json=result)

    return jsonify(result), 200
