from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    gender=db.Column(db.String(200), nullable=False)
    height=db.Column(db.String(200), nullable=False)
    birth_year=db.Column(db.String(100), nullable=False)
    hair_color=db.Column(db.String(200), nullable=False)
    skin_color=db.Column(db.String(200), nullable=False)
    eye_color=db.Column(db.String(200), nullable=False)

    def serialize(self) :
        return {
           "id": self.id,
           "name":self.id,
           "gender":self.gender,
           "height": self.height,
           "birth_year":self.birth_year,
           "hair_color":self.hair_color,
           "skin_color":self.skin_color,
           "eye_color":self.eye_color,
        }
class Planets(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(400),nullable=False)
    diameter=db.Column(db.Integer,nullable=False)
    climate=db.Column(db.String(400),nullable=False)
    gravity=db.Column(db.String(400),nullable=False)
    terrain=db.Column(db.String(400),nullable=False)
    population=db.Column(db.Integer,nullable=False)
    
    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "diameter":self.diameter,
            "climate":self.climate,
            "gravity":self.gravity,
            "terrain":self.terrain,
            "population":self.population,
        }
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('my_favorite_list', lazy='dynamic'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people = db.relationship('People', backref=db.backref('my_favorite_list', lazy='dynamic'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship('Planets', backref=db.backref('my_favorite_list', lazy='dynamic'))
  
  

    def serialize(self):
        return{
            "user_id":self.user.id,
            "people_id":self.people_id,
            "planets_id":self.planets_id,
        }
