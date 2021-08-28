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
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
