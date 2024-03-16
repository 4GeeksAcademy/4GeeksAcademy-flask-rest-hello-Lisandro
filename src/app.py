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
from models import db, User, People, Planets, Favorites #importamos las tablas que usaremos 
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


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

# a partir de aquí haremos nuestros ENDPOINTS

# ENDPOINt para que traiga todos los characters de nuestra base de datos
@app.route('/people', methods=['GET'])
def get_all_people():
    people_query = People.query.all() # siempre poner el query. Este codigo busca de la tabla people todos los characters. Te lo devuelve en crudo.
    # Haremos un list() y un map a los items que consultes (item.serialize) y como segundo valor del map es el array que mapear.
    people_data = list(map(lambda item: item.serialize(), people_query)) # procesamos la info y la devolvemos en un array
    # serialize es para que no te aparezca como <>, si no le información.
    print(people_data)
    
    # Si lo que recibimos es un array vacio, devolveremos el error 404 con el mensaje People not found
    if people_data == []:
        return jsonify({
            "msg": "Character not found"
        }), 404
    
    response_body = {
        "msg": "ok",
        "people": people_data
    }
    return jsonify(response_body), 200


# obtener los datos de un solo personaje
@app.route('/people/<int:people_id>', methods=['GET'])
# Pasarle el mismo dato (id) a la función como parametro
# Probar con el print(people_id) y comprobar endpoint en postman colocando cualquier ID 
# Si devuelve ok aparecerá en la consola de vscode el numero de id.
def get_one_people(people_id):
    people_query = People.query.filter_by(id = people_id).first() #El filter sera con el id, no se podrá repetir
    # Te lo devuelve en crudo.
    # print(people_query)
    
    if people_query == None:
        return jsonify({
            "msg": "Character not found"
        }), 404
    
    response_body = {
        "msg": "ok",
        "people": people_query.serialize() #Hacemos el serialize para mostrar la informacion tratada.
    }
    return jsonify(response_body), 200


# obtener todo los planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets_query = Planets.query.all() 
    planets_data = list(map(lambda item: item.serialize(), planets_query))
    # print(planets_query)
    
    if planets_data == []:
        return jsonify({
            "msg": "Planets not found"
        }), 404
    
    response_body = {
        "msg": "ok",
        "Planet": planets_data
    }
    return jsonify(response_body), 200


# obtener los datos de un solo planeta
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet_query = Planets.query.filter_by(id = planet_id).first() #estamos haciendo una consulta a la User para que traiga todos
    print(planet_query)
    
    if planet_query == None:
        return jsonify({
            "msg": "Planet not found"
        }), 404
    
    response_body = {
        "msg": "ok",
        "people": planet_query.serialize()
    }
    return jsonify(response_body), 200


# obtener todo los usuarios
@app.route('/user', methods=['GET'])
def get_all_users():
    user_query = User.query.all() #estamos haciendo una consulta a la User para que traiga todos
    user_data = list(map(lambda item: item.serialize(), user_query))#procesamos la info consultada y la volvemos un array
    # print(user_query)
    
    if user_data == []:
        return jsonify({
            "msg": "User not found"
        }), 404
    
    response_body = {
        "msg": "ok",
        "User": user_data
    }
    return jsonify(response_body), 200


# obten los favoritos de todos los usuarios
# Se nos pide que aparezca solo el favorito del usuario
# Hemos modificado el modelo favorites en models.py
@app.route('/user/favorites/', methods=['GET'])
@jwt_required() #traemos el token
def get_user_favorites():
# obtenermos la identity del usuario actual
    current_user = get_jwt_identity()

# buscamos el usuario dentro del modelo User
    user_query = User.query.filter_by(name=current_user).first()
# si no lo encontramos
    if not user_query:
        return jsonify({"msg": "The user hasn't been found"}), 404

# Obtenemos los favoritos del usuario actual
    user_favorites_query = Favorites.query.filter_by(id_user=user_query.id).all() #traeme todos los favoritos del id_user
    user_favorites_query_data = list(map(lambda item: item.serialize(), user_favorites_query))  #hazme un map y muestralos

    # Si no hay favoritos
    if not user_favorites_query:
        return jsonify({"msg": "There aren't any favorites yet"}), 404

    response_body = {
        "msg": "ok",
        "favorites": user_favorites_data
    }

    return jsonify(response_body), 200

###########
# Este codigo sería para traer todos los favoritos de todos los usarios
    # Aqui creamos una variable para traer todos los users
    user_favorites_query = User.query.all()
    # Aquí hacemos un map de los filter 
    user_favorites_data = list(map(lambda item: item.serialize(), user_favorites_query)) #estamos haciendo una consulta a la User para que traiga todos
    # print(user_favorites_data)
    
    if user_favorites_data == []:
        return jsonify({
            "msg": "There are no favorites on the list"
        }), 404
    
    response_body = {
        "msg": "ok",
        "User": user_favorites_data
    }
    return jsonify(response_body), 200


# añade un planeta favorito al usuario actual
@app.route('/favorites/planets/<int:id_planet>', methods=['POST'])
def add_favorite_planet_to_user(id_planet):
    # Necesitamos la siguiente linea
    body = request.json
    # Una vez nos llegue tenemos que procesar la info en la base de datos
    # Creamos variable y le pasamos los param (el id  del user que estámos usando) y el id del planeta que queremos en fav.
    new_favorite_planet = Favorites(id_user = body["id_user"], id_planets = id_planet)
    # Le decimos que lo agregue y que lo comitee 
    db.session.add(new_favorite_planet)
    db.session.commit()
    # creamos el person en postman y miramos en la base de datos a ver recargamos pagina si no sale para que se actualice.
    # print(new_favorite_planet)

    # if new_favorit_planet == "-":
    #     return jsonify({
    #         "msg": "User not found"
    #     }), 404
    
    response_body = {
        "msg": "the planet has been added to Favorites",
    }
    return jsonify(response_body), 200


# añade un personaje favorito al usuario actual
@app.route('/favorites/people/<int:id_people>', methods=['POST'])
def add_favorite_people_to_user(id_people):

    body = request.json

    new_favorite_people = Favorites(id_user = body["id_user"], id_people = id_people)
    db.session.add(new_favorite_people)
    db.session.commit()
    print(new_favorite_people)

    # if new_favorit_people == "-":
    #     return jsonify({
    #         "msg": "User not found"
    #     }), 404
    
    response_body = {
        "msg": "the character has been added to Favorites",
    }
    return jsonify(response_body), 200


# elimina un planeta favorito al usuario actual
@app.route('/favorites/planets/<int:id_planet>', methods=['DELETE'])
def delete_favorite_planet_to_user(id_planet):

    body = request.json

    delete_favorite_planet = Favorites.query.filter_by(id_planets = id_planet).first()
    db.session.delete(delete_favorite_planet)
    db.session.commit()

    # if new_favorite_planet == "-":
    #     return jsonify({
    #         "msg": "User not found"
    #     }), 404
    
    response_body = {
        "msg": "the planet has been deleted from Favorites",
    }
    return jsonify(response_body), 200


# elimina un personaje favorito
@app.route('/favorites/people/<int:id_people>', methods=['DELETE'])
def delete_favorite_people_to_user(id_people):

    body = request.json

    delete_favorite_people = Favorites.query.filter_by(id_people = id_people).first()
    db.session.delete(delete_favorite_people)
    db.session.commit()
    # print(delete_favorite_planet)

    # if delete_favorite_planet == "-":
    #      return jsonify({
    #          "msg": "User not found"
    #      }), 404
    
    response_body = {
        "msg": "the character has been deleted from Favorites",
    }
    return jsonify(response_body), 200

# creamos el endpoint para crear usuario
@app.route('/signup', methods=['POST'])
def signup():
    # El request_body o cuerpo de la solicitud ya está decodificado en formato JSON y se encuentra en la variable request.json
    request_body = request.json
    # Creamos variable y se la metemos dentro de user(Como otra instancia, cada user es una)
    # le damos como valores a name y password los request que pondremos en el Postman
    new_user = User(
        name= request_body["name"],
        password= request_body["password"],
        )
    # Le decimos que lo agregue y que lo comitee 
    db.session.add(new_user)
    db.session.commit()

    # generamos el token de este usuario
    access_token = create_access_token(identity=new_user.name)

    response_body = {
        "msg": "the user has been created",
        "access_token": access_token
    }

    return jsonify(response_body), 200


# creamos el endpoint que nos permite hacer el login  
# Para que la app sepa que el usuario es el, tendremos que hacer rutas protegidas especificadas en la documentación
@app.route("/login", methods=["POST"])
def login():
    # Las variables tienen que cuadrar con las característica del modelo de User
    name = request.json.get("name", None)
    password = request.json.get("password", None)
    # Para acceder a un usuario de nuestra tabla, tendremos que hacer un find en una variable para que nos aparezca con el filter por el nombre
    user_query = User.query.filter_by(name=name).first()

    if name != user_query.name or password != user_query.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=name)
    return jsonify(access_token=access_token)


# ENDPOINT de la ruta protegida
@app.route("/profile", methods=["GET"])
# Esta linea siempre irá aquí para traernos el token que se nos ha facilitado 
@jwt_required()
def protected():
    # metemos en una variable el usuario que esta activo
    current_user = get_jwt_identity()
    # creamos variable donde filtramos en la tabla user el actual usuario 
    info_user_favorites = User.query.filter_by(name=current_user).first()

    # devolvemos el usuario con la informacion de favoritos 
    return jsonify({"user": info_user_favorites.serialize()}), 200



if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
