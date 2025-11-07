from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from code.utils.redis_helpers import is_token_blacklisted
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return is_token_blacklisted(jti)
# Import routes
from code.routes.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route('/')
def home():
    return "🚀 Wenex API is running!!"
