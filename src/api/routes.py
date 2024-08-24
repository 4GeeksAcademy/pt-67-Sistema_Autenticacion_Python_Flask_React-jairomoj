"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# Tengo que definir mis rutas aquí y usar api en vez de app

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    email = body['email']
    password = body['password']

    if not body:
        return jsonify({"msg": "El cuerpo de la solicitud está vacío"}), 400
    if 'email' not in body:
        return jsonify({"msg": 'Debes especificar un correo electrónico (email)'}), 400
    if 'password' not in body:
        return jsonify({"msg": 'Debes especificar una contraseña (password)'}), 400

    user = User.query.filter_by(email = email).first()

    if email != user.email or password != user.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity = email)
    return jsonify(access_token = access_token)

@api.route('/signup', methods=['POST'])
def signup():
    body = request.json
    email = body['email']
    password = body['password']

    if body is None:
        return "El cuerpo de la solicitud es null", 400
    if 'email' not in body:
        return 'Debes especificar el email', 400
    if 'password' not in body:
        return 'Debes especificar una contraseña', 400

    user = User(email = email, password = password, is_active = True)
    db.session.add(user)
    db.session.commit()

    response_body = {
        "msg": "User created!"
    }

    return jsonify(response_body), 200

@api.route('/private', methods=['GET'])
@jwt_required()
def getAllUserOrders():
    # recuperar usuario
    current_user = get_jwt_identity()
    user = User.query.filter_by(email = current_user).first()

    return jsonify(logged_in_as = current_user), 200