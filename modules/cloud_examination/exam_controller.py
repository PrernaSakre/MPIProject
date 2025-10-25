from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..app import db

exam_bp = Blueprint("exam", __name__)


@exam_bp.route("/", methods=["POST"])
@jwt_required()
def create_exam():
    """Create and schedule a new exam (admin only)."""
    identity = get_jwt_identity()
    if identity.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403
    data = request.json
    exam_id = data.get("exam_id")
    if not exam_id:
        return jsonify({"error": "exam_id required"}), 400
    db.collection("exams").document(exam_id).set(data)
    return jsonify({"success": True, "exam_id": exam_id}), 201


@exam_bp.route("/<exam_id>", methods=["GET"])
@jwt_required()
def get_exam(exam_id):
    """Fetch exam details for conduction."""
    exam = db.collection("exams").document(exam_id).get()
    if exam.exists:
        return jsonify(exam.to_dict()), 200
    return jsonify({"error": "Exam not found"}), 404
