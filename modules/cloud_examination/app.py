import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from firebase_admin import credentials, firestore, initialize_app
from .exam_controller import exam_bp
from .question_service import question_bp
from .submission_handler import submission_bp
from .evaluation_engine import evaluation_bp
from .proctoring import proctoring_bp  # NEW: Proctoring blueprint

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY", "your-secret-key"
)  # Replace with env var
jwt = JWTManager(app)

# Initialize Firebase
cred = credentials.Certificate(
    "firebase_key.json"
)  # Replace with your service account key
initialize_app(cred)
db = firestore.client()

# Register blueprints
app.register_blueprint(exam_bp, url_prefix="/exams")
app.register_blueprint(question_bp, url_prefix="/questions")
app.register_blueprint(submission_bp, url_prefix="/submissions")
app.register_blueprint(evaluation_bp, url_prefix="/evaluations")
app.register_blueprint(proctoring_bp, url_prefix="/proctoring")  # NEW


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {"role": "user"}  # Customize based on user role (admin/student)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
