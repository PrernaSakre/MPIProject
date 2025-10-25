from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..app import db

submission_bp = Blueprint("submission", __name__)


@submission_bp.route("/<exam_id>", methods=["POST"])
@jwt_required()
def submit_responses(exam_id):
    """Collect and store user responses."""
    identity = get_jwt_identity()
    user_id = identity.get("sub")  # Assuming JWT sub is user_id
    data = request.json
    responses = data.get("responses")
    if not user_id or not responses:
        return jsonify({"error": "user_id and responses required"}), 400

    submission_id = f"{exam_id}_{user_id}"
    db.collection("submissions").document(submission_id).set(
        {
            "exam_id": exam_id,
            "user_id": user_id,
            "responses": responses,
            "timestamp": firestore.SERVER_TIMESTAMP,
        }
    )
    return jsonify({"success": True, "submission_id": submission_id}), 201
