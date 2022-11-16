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
from models import db, User
import flask
from flask import Flask,request
import json
#from models import Person

app = Flask(__name__)





peoples =  [
    
    {       "id": 1,
			"name": "Luke Skywalker",
			"height": "172",
			"mass": "77",
			"hair_color": "blond",
			"skin_color": "fair",
			"eye_color": "blue",
			"birth_year": "19BBY",
			"gender": "male",
			"homeworld": "https://swapi.dev/api/planets/1/",
			"films": [
				"https://swapi.dev/api/films/1/",
				"https://swapi.dev/api/films/2/",
				"https://swapi.dev/api/films/3/",
				"https://swapi.dev/api/films/6/"
			],
			"species": [],
			"vehicles": [
				"https://swapi.dev/api/vehicles/14/",
				"https://swapi.dev/api/vehicles/30/"
			],
			"starships": [
				"https://swapi.dev/api/starships/12/",
				"https://swapi.dev/api/starships/22/"
			],
			"created": "2014-12-09T13:50:51.644000Z",
			"edited": "2014-12-20T21:17:56.891000Z",
			"url": "https://swapi.dev/api/people/1/"
		},
		{
            "id": 2,
			"name": "C-3PO",
			"height": "167",
			"mass": "75",
			"hair_color": "n/a",
			"skin_color": "gold",
			"eye_color": "yellow",
			"birth_year": "112BBY",
			"gender": "n/a",
			"homeworld": "https://swapi.dev/api/planets/1/",
			"films": [
				"https://swapi.dev/api/films/1/",
				"https://swapi.dev/api/films/2/",
				"https://swapi.dev/api/films/3/",
				"https://swapi.dev/api/films/4/",
				"https://swapi.dev/api/films/5/",
				"https://swapi.dev/api/films/6/"
			],
			"species": [
				"https://swapi.dev/api/species/2/"
			],
			"vehicles": [],
			"starships": [],
			"created": "2014-12-10T15:10:51.357000Z",
			"edited": "2014-12-20T21:17:50.309000Z",
			"url": "https://swapi.dev/api/people/2/"
		},
		{
            "id": 3,
			"name": "R2-D2",
			"height": "96",
			"mass": "32",
			"hair_color": "n/a",
			"skin_color": "white, blue",
			"eye_color": "red",
			"birth_year": "33BBY",
			"gender": "n/a",
			"homeworld": "https://swapi.dev/api/planets/8/",
			"films": [
				"https://swapi.dev/api/films/1/",
				"https://swapi.dev/api/films/2/",
				"https://swapi.dev/api/films/3/",
				"https://swapi.dev/api/films/4/",
				"https://swapi.dev/api/films/5/",
				"https://swapi.dev/api/films/6/"
			],
			"species": [
				"https://swapi.dev/api/species/2/"
			],
			"vehicles": [],
			"starships": [],
			"created": "2014-12-10T15:11:50.376000Z",
			"edited": "2014-12-20T21:17:50.311000Z",
			"url": "https://swapi.dev/api/people/3/"
		},
		{
            "id": 4,
			"name": "Darth Vader",
			"height": "202",
			"mass": "136",
			"hair_color": "none",
			"skin_color": "white",
			"eye_color": "yellow",
			"birth_year": "41.9BBY",
			"gender": "male",
			"homeworld": "https://swapi.dev/api/planets/1/",
			"films": [
				"https://swapi.dev/api/films/1/",
				"https://swapi.dev/api/films/2/",
				"https://swapi.dev/api/films/3/",
				"https://swapi.dev/api/films/6/"
			],
			"species": [],
			"vehicles": [],
			"starships": [
				"https://swapi.dev/api/starships/13/"
			],
			"created": "2014-12-10T15:18:20.704000Z",
			"edited": "2014-12-20T21:17:50.313000Z",
			"url": "https://swapi.dev/api/people/4/"
		},
		{
            "id": 5,
			"name": "Leia Organa",
			"height": "150",
			"mass": "49",
			"hair_color": "brown",
			"skin_color": "light",
			"eye_color": "brown",
			"birth_year": "19BBY",
			"gender": "female",
			"homeworld": "https://swapi.dev/api/planets/2/",
			"films": [
				"https://swapi.dev/api/films/1/",
				"https://swapi.dev/api/films/2/",
				"https://swapi.dev/api/films/3/",
				"https://swapi.dev/api/films/6/"
			],
			"species": [],
			"vehicles": [
				"https://swapi.dev/api/vehicles/30/"
			],
			"starships": [],
			"created": "2014-12-10T15:20:09.791000Z",
			"edited": "2014-12-20T21:17:50.315000Z",
			"url": "https://swapi.dev/api/people/5/"
		},
		{
            "id": 6,
			"name": "Owen Lars",
			"height": "178",
			"mass": "120",
			"hair_color": "brown, grey",
			"skin_color": "light",
			"eye_color": "blue",
			"birth_year": "52BBY",
			"gender": "male",
			"homeworld": "https://swapi.dev/api/planets/1/",
			"films": [
				"https://swapi.dev/api/films/1/",
				"https://swapi.dev/api/films/5/",
				"https://swapi.dev/api/films/6/"
			],
			"species": [],
			"vehicles": [],
			"starships": [],
			"created": "2014-12-10T15:52:14.024000Z",
			"edited": "2014-12-20T21:17:50.317000Z",
			"url": "https://swapi.dev/api/people/6/"
		},
		{
            "id":7,
			"name": "Beru Whitesun lars",
			"height": "165",
			"mass": "75",
			"hair_color": "brown",
			"skin_color": "light",
			"eye_color": "blue",
			"birth_year": "47BBY",
			"gender": "female",
			"homeworld": "https://swapi.dev/api/planets/1/",
			"films": [
				"https://swapi.dev/api/films/1/",
				"https://swapi.dev/api/films/5/",
				"https://swapi.dev/api/films/6/"
			],
			"species": [],
			"vehicles": [],
			"starships": [],
			"created": "2014-12-10T15:53:41.121000Z",
			"edited": "2014-12-20T21:17:50.319000Z",
			"url": "https://swapi.dev/api/people/7/"
		},
		{
            "id": 8,
			"name": "R5-D4",
			"height": "97",
			"mass": "32",
			"hair_color": "n/a",
			"skin_color": "white, red",
			"eye_color": "red",
			"birth_year": "unknown",
			"gender": "n/a",
			"homeworld": "https://swapi.dev/api/planets/1/",
			"films": [
				"https://swapi.dev/api/films/1/"
			],
			"species": [
				"https://swapi.dev/api/species/2/"
			],
			"vehicles": [],
			"starships": [],
			"created": "2014-12-10T15:57:50.959000Z",
			"edited": "2014-12-20T21:17:50.321000Z",
			"url": "https://swapi.dev/api/people/8/"
		},
		{
            "id": 9,
			"name": "Biggs Darklighter",
			"height": "183",
			"mass": "84",
			"hair_color": "black",
			"skin_color": "light",
			"eye_color": "brown",
			"birth_year": "24BBY",
			"gender": "male",
			"homeworld": "https://swapi.dev/api/planets/1/",
			"films": [
				"https://swapi.dev/api/films/1/"
			],
			"species": [],
			"vehicles": [],
			"starships": [
				"https://swapi.dev/api/starships/12/"
			],
			"created": "2014-12-10T15:59:50.509000Z",
			"edited": "2014-12-20T21:17:50.323000Z",
			"url": "https://swapi.dev/api/people/9/"
		},
		{
            "id": 9,
			"name": "Obi-Wan Kenobi",
			"height": "182",
			"mass": "77",
			"hair_color": "auburn, white",
			"skin_color": "fair",
			"eye_color": "blue-gray",
			"birth_year": "57BBY",
			"gender": "male",
			"homeworld": "https://swapi.dev/api/planets/20/",
			"films": [
				"https://swapi.dev/api/films/1/",
				"https://swapi.dev/api/films/2/",
				"https://swapi.dev/api/films/3/",
				"https://swapi.dev/api/films/4/",
				"https://swapi.dev/api/films/5/",
				"https://swapi.dev/api/films/6/"
			],
			"species": [],
			"vehicles": [
				"https://swapi.dev/api/vehicles/38/"
			],
			"starships": [
				"https://swapi.dev/api/starships/48/",
				"https://swapi.dev/api/starships/59/",
				"https://swapi.dev/api/starships/64/",
				"https://swapi.dev/api/starships/65/",
				"https://swapi.dev/api/starships/74/"
			],
			"created": "2014-12-10T16:16:29.192000Z",
			"edited": "2014-12-20T21:17:50.325000Z",
			"url": "https://swapi.dev/api/people/10/"
		}
        
	]
    
planets = [ {
            "id": 1,
			"name": "Tatooine",
			"rotation_period": "23",
			"orbital_period": "304",
			"diameter": "10465",
			"climate": "arid",
			"gravity": "1 standard",
			"terrain": "desert",
			"surface_water": "1",
			"population": "200000",
			"residents": [
				"https://swapi.dev/api/people/1/",
				"https://swapi.dev/api/people/2/",
				"https://swapi.dev/api/people/4/",
				"https://swapi.dev/api/people/6/",
				"https://swapi.dev/api/people/7/",
				"https://swapi.dev/api/people/8/",
				"https://swapi.dev/api/people/9/",
				"https://swapi.dev/api/people/11/",
				"https://swapi.dev/api/people/43/",
				"https://swapi.dev/api/people/62/"
			],
			"films": [
				"https://swapi.dev/api/films/1/",
				"https://swapi.dev/api/films/3/",
				"https://swapi.dev/api/films/4/",
				"https://swapi.dev/api/films/5/",
				"https://swapi.dev/api/films/6/"
			],
			"created": "2014-12-09T13:50:49.641000Z",
			"edited": "2014-12-20T20:58:18.411000Z",
			"url": "https://swapi.dev/api/planets/1/"
		},
		{	"id": 2,
			"name": "Alderaan",
			"rotation_period": "24",
			"orbital_period": "364",
			"diameter": "12500",
			"climate": "temperate",
			"gravity": "1 standard",
			"terrain": "grasslands, mountains",
			"surface_water": "40",
			"population": "2000000000",
			"residents": [
				"https://swapi.dev/api/people/5/",
				"https://swapi.dev/api/people/68/",
				"https://swapi.dev/api/people/81/"
			],
			"films": [
				"https://swapi.dev/api/films/1/",
				"https://swapi.dev/api/films/6/"
			],
			"created": "2014-12-10T11:35:48.479000Z",
			"edited": "2014-12-20T20:58:18.420000Z",
			"url": "https://swapi.dev/api/planets/2/"
		},
		{   "id": 3,
			"name": "Yavin IV",
			"rotation_period": "24",
			"orbital_period": "4818",
			"diameter": "10200",
			"climate": "temperate, tropical",
			"gravity": "1 standard",
			"terrain": "jungle, rainforests",
			"surface_water": "8",
			"population": "1000",
			"residents": [],
			"films": [
				"https://swapi.dev/api/films/1/"
			],
			"created": "2014-12-10T11:37:19.144000Z",
			"edited": "2014-12-20T20:58:18.421000Z",
			"url": "https://swapi.dev/api/planets/3/"
		},
		{
            "id": 4,
			"name": "Hoth",
			"rotation_period": "23",
			"orbital_period": "549",
			"diameter": "7200",
			"climate": "frozen",
			"gravity": "1.1 standard",
			"terrain": "tundra, ice caves, mountain ranges",
			"surface_water": "100",
			"population": "unknown",
			"residents": [],
			"films": [
				"https://swapi.dev/api/films/2/"
			],
			"created": "2014-12-10T11:39:13.934000Z",
			"edited": "2014-12-20T20:58:18.423000Z",
			"url": "https://swapi.dev/api/planets/4/"
		},
		{
            "id": 5,
			"name": "Dagobah",
			"rotation_period": "23",
			"orbital_period": "341",
			"diameter": "8900",
			"climate": "murky",
			"gravity": "N/A",
			"terrain": "swamp, jungles",
			"surface_water": "8",
			"population": "unknown",
			"residents": [],
			"films": [
				"https://swapi.dev/api/films/2/",
				"https://swapi.dev/api/films/3/",
				"https://swapi.dev/api/films/6/"
			],
			"created": "2014-12-10T11:42:22.590000Z",
			"edited": "2014-12-20T20:58:18.425000Z",
			"url": "https://swapi.dev/api/planets/5/"
		},
		{
            "id": 6,
			"name": "Bespin",
			"rotation_period": "12",
			"orbital_period": "5110",
			"diameter": "118000",
			"climate": "temperate",
			"gravity": "1.5 (surface), 1 standard (Cloud City)",
			"terrain": "gas giant",
			"surface_water": "0",
			"population": "6000000",
			"residents": [
				"https://swapi.dev/api/people/26/"
			],
			"films": [
				"https://swapi.dev/api/films/2/"
			],
			"created": "2014-12-10T11:43:55.240000Z",
			"edited": "2014-12-20T20:58:18.427000Z",
			"url": "https://swapi.dev/api/planets/6/"
		},
		{
            "id": 7,
			"name": "Endor",
			"rotation_period": "18",
			"orbital_period": "402",
			"diameter": "4900",
			"climate": "temperate",
			"gravity": "0.85 standard",
			"terrain": "forests, mountains, lakes",
			"surface_water": "8",
			"population": "30000000",
			"residents": [
				"https://swapi.dev/api/people/30/"
			],
			"films": [
				"https://swapi.dev/api/films/3/"
			],
			"created": "2014-12-10T11:50:29.349000Z",
			"edited": "2014-12-20T20:58:18.429000Z",
			"url": "https://swapi.dev/api/planets/7/"
		},
		{
            "id": 8,
			"name": "Naboo",
			"rotation_period": "26",
			"orbital_period": "312",
			"diameter": "12120",
			"climate": "temperate",
			"gravity": "1 standard",
			"terrain": "grassy hills, swamps, forests, mountains",
			"surface_water": "12",
			"population": "4500000000",
			"residents": [
				"https://swapi.dev/api/people/3/",
				"https://swapi.dev/api/people/21/",
				"https://swapi.dev/api/people/35/",
				"https://swapi.dev/api/people/36/",
				"https://swapi.dev/api/people/37/",
				"https://swapi.dev/api/people/38/",
				"https://swapi.dev/api/people/39/",
				"https://swapi.dev/api/people/42/",
				"https://swapi.dev/api/people/60/",
				"https://swapi.dev/api/people/61/",
				"https://swapi.dev/api/people/66/"
			],
			"films": [
				"https://swapi.dev/api/films/3/",
				"https://swapi.dev/api/films/4/",
				"https://swapi.dev/api/films/5/",
				"https://swapi.dev/api/films/6/"
			],
			"created": "2014-12-10T11:52:31.066000Z",
			"edited": "2014-12-20T20:58:18.430000Z",
			"url": "https://swapi.dev/api/planets/8/"
		},
		{
            "id": 9,
			"name": "Coruscant",
			"rotation_period": "24",
			"orbital_period": "368",
			"diameter": "12240",
			"climate": "temperate",
			"gravity": "1 standard",
			"terrain": "cityscape, mountains",
			"surface_water": "unknown",
			"population": "1000000000000",
			"residents": [
				"https://swapi.dev/api/people/34/",
				"https://swapi.dev/api/people/55/",
				"https://swapi.dev/api/people/74/"
			],
			"films": [
				"https://swapi.dev/api/films/3/",
				"https://swapi.dev/api/films/4/",
				"https://swapi.dev/api/films/5/",
				"https://swapi.dev/api/films/6/"
			],
			"created": "2014-12-10T11:54:13.921000Z",
			"edited": "2014-12-20T20:58:18.432000Z",
			"url": "https://swapi.dev/api/planets/9/"
		},
		{
            "id": 10,
			"name": "Kamino",
			"rotation_period": "27",
			"orbital_period": "463",
			"diameter": "19720",
			"climate": "temperate",
			"gravity": "1 standard",
			"terrain": "ocean",
			"surface_water": "100",
			"population": "1000000000",
			"residents": [
				"https://swapi.dev/api/people/22/",
				"https://swapi.dev/api/people/72/",
				"https://swapi.dev/api/people/73/"
			],
			"films": [
				"https://swapi.dev/api/films/5/"
			],
			"created": "2014-12-10T12:45:06.577000Z",
			"edited": "2014-12-20T20:58:18.434000Z",
			"url": "https://swapi.dev/api/planets/10/"
		}]

favoritos=[{"name":"Luke Skywalker"},{"name":"Kamino"}]
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
        "user": "martin"
    }

    return jsonify(response_body), 200


@app.route('/peoples', methods=['GET'])
def personajes():
   
 

    # puedes convertir esa variable en un string json así
    json_text = flask.jsonify(peoples)

    # y luego puedes retornarla (return) en el response body así:
    return json_text

@app.route('/users/favorites', methods=['GET'])
def favorites():
   
 

    # puedes convertir esa variable en un string json así
    json_text = flask.jsonify(favoritos)

    # y luego puedes retornarla (return) en el response body así:
    return json_text

@app.route('/planets', methods=['GET'])
def planetas():
   
 

    # puedes convertir esa variable en un string json así
    json_text = flask.jsonify(planets)

    # y luego puedes retornarla (return) en el response body así:
    return json_text
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
	planetFound=[id for id in planets if id["id"] == planet_id]
	return jsonify({"planeta": planetFound})


@app.route('/peoples/<int:people_id>', methods=['GET'])
def get_people(people_id):
	peopleFound=[id for id in peoples if id["id"]==people_id]
	return jsonify({"personaje": peopleFound})


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_new_pl():
    request_body = request.data
    print("Incoming request with the following body", request_body)
    decoded_object = json.loads(request.data)
    favoritos.append(decoded_object)
    json_textt = flask.jsonify(favoritos)
    return  json_textt

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_new_p():
    request_body = request.data
    print("Incoming request with the following body", request_body)
    decoded_object = json.loads(request.data)
    favoritos.append(decoded_object)
    json_textt = flask.jsonify(favoritos)
    return  json_textt



@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_pl(position):
    print("This is the position to delete: ",position)
    del favoritos[position]
    json_texttt = flask.jsonify(favoritos)
    return json_texttt

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_p(position):
    print("This is the position to delete: ",position)
    del favoritos[position]
    json_texttt = flask.jsonify(favoritos)
    return json_texttt

@app.route('/users/favorites', methods=['POST'])
def add_new_pll():
    request_body = request.data
    print("Incoming request with the following body", request_body)
    decoded_object = json.loads(request.data)
    favoritos.append(decoded_object)
    json_textt = flask.jsonify(favoritos)
    return  json_textt


    
  

    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
