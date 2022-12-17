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
from models import db, User, Characters, Planets, Favorite_Characters, Favorite_Planets
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

    users_query = User.query.all()

    all_user = list(map(lambda x: x.serialize(), users_query))

    return jsonify(all_user), 200

@app.route('/user', methods=['POST'])
def createUser():

    body = request.get_json()
    if body is None:
        return "The request body is null", 400
    if 'email' not in body:
        return "Add the user email", 400
    if 'password' not in body:
        return "Add user password", 400
    if 'Is_active' not in body:
        return "Add if the user is active", 400

    new_user = User(email=body["email"], password=body["password"], is_active=body["Is_active"])
    db.session.add(new_user)   
    db.session.commit()             
    
    return 'User was added', 200

@app.route('/user/<int:id>', methods=['PUT'])
def updateUser(id):
    user1 = User.query.get(id)

    body = request.get_json()
    
    if body == None:
        return 'Body is empty', 400
    if 'email' not in body:
        return "Add the user email", 400

    user1.email = body["email"]
    db.session.commit()            
    
    return 'ok'

@app.route('/user/<int:id>', methods=['DELETE'])
def deleteUser(id):
    user1 = User.query.get(id)
    if user1 == None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()  
    return 'User deleted'

@app.route('/people', methods=['GET'])
def getCharacters():

    people_query = Characters.query.all()

    all_characters = list(map(lambda x: x.serialize(), people_query))

    return jsonify(all_characters), 200

@app.route('/people', methods=['POST'])
def addCharacter():

    body = request.get_json()
    if body is None:
        return "The request body is null", 400
    if 'name' not in body:
        return "Add the character's name", 400
    if 'birth_year' not in body:
        return "Add character's birth year", 400
    if 'gender' not in body:
        return "Add character's gender", 400
    if 'hair_color' not in body:
        return "Add character's hair color", 400
    if 'eye_color' not in body:
        return "Add character's eye color", 400        

    new_character = Characters(name=body["name"], birth_year=body["birth_year"], gender=body["gender"], hair_color=body["hair_color"], eye_color=body["eye_color"])
    db.session.add(new_character)   
    db.session.commit()             
    
    return 'Character was added', 200

@app.route('/people/<int:id>', methods=['PUT'])
def updateCharacter(id):
    character1 = Characters.query.get(id)

    body = request.get_json()
    
    if body == None:
        return 'Body is empty', 400
    if 'name' in body:
        return "Name cannot be edited", 400
    if 'birth_year' in body:
        character1.birth_year = body["birth_year"]
    if 'gender' in body:
        character1.gender = body["gender"]
    if 'hair_color' in body:
        character1.hair_color = body["hair_color"]
    elif 'eye_color' in body:
        character1.eye_color = body["eye_color"]            

    db.session.commit()            
    
    return "Character's data has been updated", 200   

@app.route('/people/<int:id>', methods=['GET'])
def getCharacter(id):

    character_query = Characters.query.get(id)

    if character_query == None:
        raise APIException('Character does not exist', status_code=404)    

    return jsonify(character_query.serialize()), 200

@app.route('/people/<int:id>', methods=['DELETE'])
def deleteCharacter(id):
    character1 = Characters.query.get(id)
    if character1 == None:
        raise APIException('Character not found', status_code=404)
    db.session.delete(character1)
    db.session.commit()  
    return 'Character deleted'    

@app.route('/planets', methods=['GET'])
def getPlanets():

    planets_query = Planets.query.all()

    all_planets = list(map(lambda x: x.serialize(), planets_query))

    return jsonify(all_planets), 200

@app.route('/planets', methods=['POST'])
def addPlanet():

    body = request.get_json()
    if body is None:
        return "The request body is null", 400
    if 'name' not in body:
        return "Add the planet's name", 400
    if 'population' not in body:
        return "Add planet's population", 400
    if 'terrain' not in body:
        return "Add planet's terrain", 400          

    new_planet = Planets(name=body["name"], population=body["population"], terrain=body["terrain"])
    db.session.add(new_planet)   
    db.session.commit()             
    
    return 'Planet was added', 200

@app.route('/planets/<int:id>', methods=['PUT'])
def updatePlanet(id):
    planet1 = Planets.query.get(id)

    body = request.get_json()
    
    if body == None:
        return 'Body is empty', 400
    if 'name' in body:
        return "Name cannot be edited", 400
    if 'population' in body:
        planet1.population = body["population"]
    elif 'terrain' in body:
        planet1.terrain = body["terrain"]
    
    db.session.commit()            
    
    return "Planet's data has been updated", 200          

@app.route('/planets/<int:id>', methods=['GET'])
def getPlanet(id):

    planet_query = Planets.query.get(id)

    if planet_query == None:
        raise APIException('Planet does not exist', status_code=404)    

    return jsonify(planet_query.serialize()), 200

@app.route('/planets/<int:id>', methods=['DELETE'])
def deletePlanet(id):
    planet1 = Planets.query.get(id)
    if planet1 == None:
        raise APIException('Planet not found', status_code=404)
    db.session.delete(planet1)
    db.session.commit()  
    return 'Planet deleted'

@app.route('/user/favorites', methods=['GET'])
def userFavorites():

    favchar_query = Favorite_Characters.query.all()
    favplat_query = Favorite_Planets.query.all()

    user_Favorites = list(map(lambda x: x.serialize(), favchar_query))
    user_Favorites1 = list(map(lambda x: x.serialize(), favplat_query))

    return jsonify(user_Favorites, user_Favorites1), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def addFavoritePlanet(planet_id):

    body = request.get_json()

    if body == None:
        return "The request body is null", 400
    if 'user_id' not in body:
        return "Add the user's ID number", 400    
    if 'planet_id' not in body:
        return "Add the character's ID number", 400

    newFav = Favorite_Planets(user_id=body["user_id"], planet_id=body["planet_id"])

    favPlat = Planets.query.get(newFav.planet_id)

    if favPlat == None:
        raise APIException('Planet does not exist', status_code=404)

    db.session.add(newFav)
    db.session.commit()

    return 'Favorite planet has been added', 200    

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def addFavoritePeople(people_id):

    body = request.get_json()

    if body == None:
        return "The request body is null", 400
    if 'user_id' not in body:
        return "Add the user's ID number", 400    
    if 'characters_id' not in body:
        return "Add the character's ID number", 400

    newFav = Favorite_Characters(user_id=body["user_id"], characters_id=body["characters_id"])

    favChar = Characters.query.get(newFav.characters_id)

    if favChar == None:
        raise APIException('Character does not exist', status_code=404)

    db.session.add(newFav)
    db.session.commit()

    return 'Favorite character has been added', 200 

@app.route('/favorite/people/<int:id>', methods=['DELETE'])
def deleteFavoriteCharacter(id):
    character1 = Favorite_Characters.query.get(id)
    if character1 == None:
        raise APIException('Character not found', status_code=404)
    db.session.delete(character1)
    db.session.commit()  
    return 'Favorite Character deleted'

@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def deleteFavoritePlanet(id):
    planet1 = Favorite_Planets.query.get(id)
    if planet1 == None:
        raise APIException('Planet not found', status_code=404)
    db.session.delete(planet1)
    db.session.commit()  
    return 'Favorite Planet deleted'           

    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
