from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    surname = db.Column(db.String(250), nullable=False)
    date_suscription = db.Column(db.DateTime)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
        }

class FavoritesPlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id= db.Column(db.Integer, ForeignKey('planet.id'))
    user_id= db.Column(db.Integer, ForeignKey('user.id'))

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
        }

class FavoritesCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id= db.Column(db.Integer, ForeignKey('character.id'))
    user_id= db.Column(db.Integer, ForeignKey('user.id'))

    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            "user_id": self.user_id
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer)
    climate = db.Column(db.String(250), nullable=False)
    orbit = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "orbit": self.orbit
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer,  nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender
        }