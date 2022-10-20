"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Planets, People, User, Favoritos
#from models import Person
import json
# import flask
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#endpoint
    # traer usuario
@app.route('/user', methods=['GET'])
def get_user():

    response_body = {
        "msg": "Aqui esta su usuario"
    }

    return jsonify(response_body), 200

    # User crear usuario

@app.route('/user', methods=['POST'])
def create_user():
    body = json.loads(request.data)
    # data = request.get_json()
    # print(data)

    query_user = User.query.filter_by(email=body["email"]).first()

    # if body["email"] == query_user.email:
    if query_user is None:
        #guardar datos recibidos a la tabla User
        new_user = User(id=body["id"],email=body["email"],password=body["password"],username=body["username"],first_Name=body["first_Name"],last_Name=body["last_Name"],birth_year=body["birth_year"],gender=body["gender"])
        db.session.add(new_user)
        db.session.commit()
        response_body = {
                "msg": "created user"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "existed user"
        }
    return jsonify(response_body), 400

    # people

@app.route('/people', methods=['GET'])
def get_all_people():

    people = People.query.all() # esto obtiene todos los registros de la tabla User
    results = list(map(lambda item: item.serialize(), people)) #esto serializa los datos del arrays users

    return jsonify(results), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):

    people = People.query.filter_by(id=people_id).first()

    return jsonify(people.serialize()), 200

    # planets

@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planets.query.all() # esto obtiene todos los registros de la tabla User
    results = list(map(lambda item: item.serialize(), planets)) #esto serializa los datos del arrays users

    return jsonify(results), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets(planets_id):

    planets = Planets.query.filter_by(id=planets_id).first()

    return jsonify(planets.serialize()), 200

    # traer un favoritos por el usuario

@app.route('/user/<int:user_id>/favoritos', methods=['GET'])
def get_favoritos(user_id):

    favoritos = Favoritos.query.filter_by(user_id=user_id).all()
    total_favoritos = list(map(lambda item: item.serialize(), favoritos))

    return jsonify(total_favoritos), 200

    # crear mi favoritos planeta

@app.route('/user/<int:user_id>/favoritos/planets', methods=['POST'])
def create_planets_favoritos(user_id):
    body = json.loads(request.data)

    query_planets_favoritos = Favoritos.query.filter_by(planets_id=body["planets_id"], user_id=body["user_id"]).first()

    if query_planets_favoritos is None:
        #guardar datos recibidos a la tabla planets_favoritos
        new_planets_favoritos = Favoritos(user_id=body["user_id"],planets_id=body["planets"],people_id=body["people"])
        db.session.add(new_planets_favoritos)
        db.session.commit()
        response_body = {
                "msg": "created planets_favoritos"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "existed planets_favoritos"
        }
    return jsonify(response_body), 400

     # crear mi favoritos people

@app.route('/user/<int:user_id>/favoritos/people', methods=['POST'])
def create_people_favoritos(user_id):
    body = json.loads(request.data)

    query_people_favoritos = Favoritos.query.filter_by(people_id=body["people_id"], user_id=body["user_id"]).first()

    if query_people_favoritos is None:
        #guardar datos recibidos a la tabla people_favoritos
        new_people_favoritos = Favoritos(user_id=body["user_id"],planets_id=body["planets"],people_id=body["people"])
        db.session.add(new_people_favoritos)
        db.session.commit()
        response_body = {
                "msg": "created people_favoritos"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "existed people_favoritos"
        }
    return jsonify(response_body), 400

    # Delete favoritos planetas

@app.route('/user/<int:user_id>/favoritos/planets', methods=['DELETE'])
def delete_planets_favoritos(user_id):
    body = json.loads(request.data)

    query_planets_favoritos = Favoritos.query.filter_by(planets_id=body["planets_id"], user_id=body["user_id"]).first()

    if query_planets_favoritos is not None:
        #guardar datos recibidos a la tabla planets_favoritos
        delete_planets_favoritos = query_planets_favoritos
        db.session.delete(delete_planets_favoritos)
        db.session.commit()

        response_body = {
                "msg": "deleted planets_favoritos"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "this planets_favoritos does not exist"
        }
    return jsonify(response_body), 400

     # Delete favoritos people

@app.route('/user/<int:user_id>/favoritos/people', methods=['DELETE'])
def delete_people_favoritos(user_id):
    body = json.loads(request.data)

    query_people_favoritos = Favoritos.query.filter_by(people_id=body["people_id"], user_id=body["user_id"]).first()

    if query_people_favoritos is not None:
        #guardar datos recibidos a la tabla people_favoritos
        delete_people_favoritos = query_people_favoritos
        db.session.delete(delete_people_favoritos)
        db.session.commit()

        response_body = {
                "msg": "deleted people_favoritos"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "this people_favoritos does not exist"
        }
    return jsonify(response_body), 400

    
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "User doesn't exist"}), 401


    if email != user.email or password != user.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    response_body = {
            "access_token": access_token,
            "user": user.serialize()
        }
    return jsonify(response_body), 200

    
# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/profile", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()

    user = User.query.filter_by(email=current_user).first()

    if user is None:
        return jsonify({"msg": "User doesn't exist"}), 401

    response_body = {
        "user": user.serialize()
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
