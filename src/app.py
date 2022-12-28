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
from models import db, User, Planet, Character, FavoritesPlanets, FavoritesCharacter
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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



#-----------------user endpoints--------------------->

@app.route('/user', methods=['GET'])
def list_users():

    users = User.query.all()
    data = [user.serialize()for user in users]

    
    return jsonify(data), 200

@app.route('/users/favorites', methods=['GET'])
def list_favorites():

    favorites_planets = FavoritesPlanets.query.all()
    data_planets = [favoritesplanets.serialize()for favoritesplanets in favorites_planets]

    favorites_characters = FavoritesCharacter.query.all()
    data_character = [favoritescharacters.serialize() for favoritescharacters in favorites_characters]

    
    return jsonify(data_planets,data_character), 200

@app.route('/favorite/planet/<int:idPlanet>',  methods=['POST'])
def add_planet_favorite(idPlanet):
    
    data = request.json

    planet = FavoritesPlanets(planet_id=data['planet_id'],user_id=data['user_id'])
    db.session.add(planet)
    db.session.commit()  
      
    return jsonify({"mensaje":"Planet favorite add"}), 200

@app.route('/favorite/character/<int:idCharacter>',  methods=['POST'])
def add_character_favorite(idCharacter):
    
    data = request.json

    character = FavoritesCharacter(character_id=data['character_id'],user_id=data['user_id'])
    db.session.add(character)
    db.session.commit()  
      
    return jsonify({"mensaje":"Character favorite add"}), 200


#-----------------planets endpoints--------------------->

@app.route('/planet', methods=['GET'])
def list_planets():       

    planets = Planet.query.all()
    data_planet = [planet.serialize()for planet in planets]

    
    return jsonify(data_planet), 200


@app.route('/planet/<int:idPlanet>', methods=['GET'])
def get_planet(idPlanet):       

    planet = Planet.query.filter_by(id=idPlanet).first()
    
    if planet:
        return jsonify(planet.serialize())

    return jsonify({"mensaje":"Planet not found"}),400


@app.route('/planet', methods=['POST'])
def create_planet():       
      data = request.json

      planet = Planet(name=data['name'],population=data['population'], climate=data['climate'], orbit=data['orbit'])
      db.session.add(planet)
      db.session.commit()  
      
      return jsonify({"mensaje":"Planeta creado"}), 200

#-----------------character endpoints--------------------->

@app.route('/character', methods=['GET'])
def list_characters():       

    characters = Character.query.all()
    data_character = [character.serialize()for character in characters]

    
    return jsonify(data_character), 200

@app.route('/character/<int:idCharacter>', methods=['GET'])
def get_character(idCharacter):       

    character = Character.query.filter_by(id=idCharacter).first()
    
    if character:
        return jsonify(character.serialize())

    return jsonify({"mensaje":"Character not found"}),400

@app.route('/character', methods=['POST'])
def create_character():     

      data = request.json

      character = Character(name=data['name'],height=data['height'], mass=data['mass'], gender=data['gender'])
      db.session.add(character)
      db.session.commit()  
      
      return jsonify({"mensaje":"Character created"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
