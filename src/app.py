"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from api.models import db, User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file


@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
# Tengo que definir mis rutas en el routes.py y en vez de usar las rutas completas, usar la variable BACKEND_URL de .env
@app.route("/login", methods=["POST"])
def login():
    print("Hola!")
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email is "" or email is None:
        return 'Debes especificar el email', 400
    if password is "" or password is None:
        return 'Debes especificar una contraseña', 400

    user = User.query.filter_by(email = email).first()

    if email != user.email or password != user.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity = email)
    return jsonify(access_token = access_token)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/private", methods=["GET"])
@jwt_required()
def private():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as = current_user), 200

@app.route('/signup', methods=['POST'])
def signup():

    body = request.json

    if body is None:
        return "El cuerpo de la solicitud es null", 400
    if 'email' not in body:
        return 'Debes especificar el email', 400
    if 'password' not in body:
        return 'Debes especificar una contraseña', 400
    if 'is_active' not in body:
        return 'Debes especificar si el usuario está activo', 400

    user = User(email = body["email"], password = body["password"], is_active = body["is_active"])
    db.session.add(user)
    db.session.commit()

    response_body = {
        "msg": "Logged out!"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
