from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

db = SQLAlchemy()
Base = declarative_base()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email            
            # do not serialize the password, its a security breach
        }

  
class Characters(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    birth_year = db.Column(db.String(100), unique=False, nullable=False)
    gender = db.Column(db.String(100), unique=False, nullable=False)
    hair_color = db.Column(db.String(100), unique=False, nullable=False)
    eye_color = db.Column(db.String(100), unique=False, nullable=False)
    Favorite_Characters = db.relationship('Favorite_Characters', lazy=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(100), unique=False, nullable=False)
    Favorite_Planets = db.relationship('Favorite_Planets', lazy=True)    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain
       }

class Favorite_Characters(db.Model):      
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))    

    def serialize(self):
        return{
            "id" : self.id,
            "user_id": self.user_id,            
            "characters_id" : self.characters_id            
        }

class Favorite_Planets(db.Model):      
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))    

    def serialize(self):
        return{
            "id" : self.id,
            "user_id" : self.user_id,
            "planet_id" : self.planet_id
        }

 
