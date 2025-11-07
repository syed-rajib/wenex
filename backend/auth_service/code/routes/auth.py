from flask import Blueprint, request, jsonify
from app import db, jwt
from ..model.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
import time
from ..utils.redis_helpers import blacklist_token


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token})
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    User logout route.
    Blacklists current JWT in Redis so it can't be used again.
    """
    jti = get_jwt()["jti"]           # JWT এর unique ID
    exp_timestamp = get_jwt()["exp"] # JWT expiration timestamp
    now = int(time.time())
    seconds_until_exp = exp_timestamp - now  # কতক্ষনের জন্য blacklist থাকবে

    # Add token JTI to Redis blacklist
    blacklist_token(jti, seconds_until_exp)

    return jsonify({"msg": "Successfully logged out"}), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({
        "username": user.username,
        "email": user.email
    })
