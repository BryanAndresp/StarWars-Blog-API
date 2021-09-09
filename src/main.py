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
from models import db, User, People, Planets, Favorites
from flask_jwt_extended import JWTManager, create_access_token
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/login', methods= ["POST"])
def sign_in():
    email= request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })

@app.route('/register', methods =["POST"])
def sign_up ():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    # validation of possible empty inputs
    if email is None:
        return jsonify({"msg": "No email was provided"}), 400
    if password is None:
        return jsonify({"msg": "No password was provided"}), 400
    # busca usuario en BBDD
    user = User.query.filter_by(email=email).first()
    if user:
        # the user was not found on the database
        return jsonify({"msg": "User already exists"}), 401
    else:
        # crea nuevo usuario
        new_user = User()
        new_user.email = email
        new_user.password = password
        # crea registro nuevo en BBDD de
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User created successfully"}), 200








@app.route('/people', methods=['GET'])
def getAllPeople():
    allpeople= People.query.all()
    allpeople= list(map(lambda People: People.serialize(),allpeople))

    return  jsonify(allpeople),200

@app.route('/people/<int:id>', methods=['GET'])
def getPeopleId(id):
    peopleId= People.query.get(id)
    if peopleId is None:
        return {'msg':'This member does not exist'}
    peopleId= People.serialize(peopleId)

    return jsonify(peopleId), 200


@app.route('/planets', methods=['GET'])
def getAllPlanets():
    allplanets= Planets.query.all()
    allplanets= list(map(lambda Planets: Planets.serialize(),allplanets))

    return  jsonify(allplanets),200


@app.route('/planets/<int:id>', methods=['GET'])
def getPlanetsId(id):
    planetsId= Planets.query.get(id)
    if planetsId is None:
        return {'msg':'This planet does not exist'}
    planetsId= Planets.serialize(planetsId)

    return jsonify(planetsId), 200

@app.route('/people', methods=['POST'])
def createPeople():
    name = request.json.get('name', None)
    gender = request.json.get('gender', None)
    height = request.json.get('height', None)
    birth_year = request.json.get('birth_year', None)
    hair_color = request.json.get('hair_color', None)
    skin_color = request.json.get('skin_color', None)
    eye_color = request.json.get('eye_color', None)
      
    if name is None:
        return jsonify({'msg':'No name was provided'}), 400
    if gender is None:
        return jsonify({'msg':'No gender was provided'}), 400
    if height is None:
        return jsonify({'msg':'No height was provided'}), 400
    if birth_year is None:
        return jsonify({'msg':'No bird year was provided'}), 400
    if skin_color is None:
        return jsonify({'msg':'No skin color was provided'}), 400
    if eye_color is None:
        return jsonify({'msg':'No eye color was provided'}), 400

    people = People.query.filter_by(name=name).first()
    if people:
       return jsonify({"msg":"people already exist"}), 401
     
    else:
         new_people = People()
         new_people.name = name
         new_people.gender = gender
         new_people.height = height
         new_people.birth_year = birth_year
         new_people.skin_color = skin_color
         new_people.hair_color = hair_color
         new_people.eye_color = eye_color
         db.session.add(new_people)
         db.session.commit()
         
         return jsonify({"msg": "people created successfully"}), 200


@app.route('/planets', methods=['POST'])
def createdPlanet():
    name = request.json.get('name', None)
    diameter = request.json.get('diameter', None)
    climate = request.json.get('climate', None)
    gravity = request.json.get('gravity', None)
    terrain= request.json.get('terrain', None)
    population = request.json.get('population', None)
      
    if name is None:
        return jsonify({'msg':'No name was provided'}), 400
    if diameter is None:
        return jsonify({'msg':'No diameter was provided'}), 400
    if climate is None:
        return jsonify({'msg':'No climate was provided'}), 400
    if gravity is None:
        return jsonify({'msg':'No gravity was provided'}), 400
    if terrain is None:
        return jsonify({'msg':'No terrain was provided'}), 400
    if population is None:
        return jsonify({'msg':'No population was provided'}), 400

    planets = Planets.query.filter_by(name=name).first()
    if planets:
        # the planet was found on the database
        return jsonify({"msg": "Planet already exists"}), 401
     
    else:
         new_planet = Planets()
         new_planet.name = name
         new_planet.diameter = diameter
         new_planet.climate = climate
         new_planet.gravity = gravity
         new_planet.terrain = terrain
         new_planet.population = population
         db.session.add(new_planet)
         db.session.commit()
         
         return jsonify({"msg": "planet created successfully"}), 200



@app.route('/people:<int:id>', methods=['DELETE'])
def deletePeople(id):
    people = People.deletePeople(id)
    return jsonify(people), 200


@app.route('/planets:<int:id>', methods=['DELETE'])
def deletePlanet(id):
       planet= Planet.deletePlanet(id)
       return jsonify (planet), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
