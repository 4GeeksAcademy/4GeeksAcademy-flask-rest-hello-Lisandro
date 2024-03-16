from flask_sqlalchemy import SQLAlchemy

# Se encarga de conectar y crear la base de datos   
db = SQLAlchemy()

# Esta será nuestra tabla padre, sin esta tabla no existen las demas.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    
    favorites_user = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    # Serialize permite retornar un objeto con los valores que queremos mostrar.
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(250), nullable=True)
    hair_color = db.Column(db.String(250), nullable=True)
    height = db.Column(db.String(250), nullable=True)
    skin_color = db.Column(db.String(250), nullable=True)
    homeworld = db.Column(db.String(250), nullable=True)
    mass = db.Column(db.String(250), nullable=True)
    created = db.Column(db.String(250), nullable=True)
    edited = db.Column(db.String(250), nullable=True)
    url = db.Column(db.String(250), nullable=True)
    # id_films = db.Column(db.Integer, ForeignKey('films.id'))
    # id_starships = db.Column(db.Integer, db.ForeignKey('starships.id'))
    id_vehicles = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    id_species = db.Column(db.Integer, db.ForeignKey('species.id'))

    # Este codigo nos ayuda a relacionar tablas. Siempre va el modelo/tabla padre la primera letra mayuscula
    #  el primer '' de donde traemos la info , el segundo la tabla que coge la info y es el nombre de la tabla en min
    # Esto genera otra columna con la información de la tabla people
    people_favorites = db.relationship('Favorites', backref='people', lazy=True)
    # En este caso traemos a la tabla people los vehiculos que cada uno utiliza.
    vehicle = db.relationship('Vehicles', backref='people', lazy=True)
    specie = db.relationship('Species', backref='people', lazy=True)
    # starships = relationship('Starships', backref='people', lazy=True)
    planets = db.relationship('Planets', backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.id

    # Serialize permite retornar un objeto con los valores que queremos mostrar.
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(250), nullable=True)
    diameter = db.Column(db.String(250), nullable=True)
    rotation_period = db.Column(db.String(250), nullable=True)
    orbital_period = db.Column(db.String(250), nullable=True)
    gravity = db.Column(db.String(250), nullable=True)
    population = db.Column(db.String(250), nullable=True)
    terrain = db.Column(db.String(250), nullable=True)
    surface_water = db.Column(db.String(250), nullable=True)
    created = db.Column(db.String(250), nullable=True)
    edited = db.Column(db.String(250), nullable=True)
    url = db.Column(db.String(250), nullable=True)
    id_people = db.Column(db.Integer, db.ForeignKey('people.id'))
    # id_films = db.Column(db.Integer, db.ForeignKey('films.id'))
    planets_favorites = db.relationship('Favorites', backref='planets', lazy=True)

    # people = db.relationship('People', backref='planets', lazy=True)


    def __repr__(self):
        return '<Planets %r>' % self.id

    # Serialize permite retornar un objeto con los valores que queremos mostrar.
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    model = db.Column(db.String(250), nullable=True)
    vehicle_class = db.Column(db.String(250), nullable=True)
    manufacturer = db.Column(db.String(250), nullable=True)
    length = db.Column(db.String(250), nullable=True)
    cost_in_credits = db.Column(db.String(250), nullable=True)
    crew = db.Column(db.String(250), nullable=True)
    passengers = db.Column(db.String(250), nullable=True)
    max_atmosphering_speed = db.Column(db.String(250), nullable=True)
    cargo_capacity = db.Column(db.String(250), nullable=True)
    consumables = db.Column(db.String(250), nullable=True)
    created = db.Column(db.String(250), nullable=True)
    edited = db.Column(db.String(250), nullable=True)
    url = db.Column(db.String(250), nullable=True)
    # id_people = db.Column(db.Integer, db.ForeignKey('people.id'))
    # id_films = db.Column(db.Integer, db.ForeignKey('films.id'))
    vehicles_favorites = db.relationship('Favorites', backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicles %r>' % self.id

    # Serialize permite retornar un objeto con los valores que queremos mostrar.
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }


class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    classification = db.Column(db.String(250), nullable=True)
    designation = db.Column(db.String(250), nullable=True)
    average_heigth = db.Column(db.String(250), nullable=True)
    average_lifespan = db.Column(db.String(250), nullable=True)
    eye_colors = db.Column(db.String(250), nullable=True)
    hair_colors = db.Column(db.String(250), nullable=True)
    skin_colors = db.Column(db.String(250), nullable=True)
    language = db.Column(db.String(250), nullable=True)
    homeworld = db.Column(db.String(250), nullable=True)
    created = db.Column(db.String(250), nullable=True)
    edited = db.Column(db.String(250), nullable=True)
    url = db.Column(db.String(250), nullable=True)
    # id_people = db.Column(db.Integer, db.ForeignKey('people.id'))
    # id_films = db.Column(db.Integer, db.ForeignKey('films.id'))
    # species_favorites = db.relationship('Favorites', backref='species', lazy=True)

    def __repr__(self):
        return '<Species %r>' % self.id

    # Serialize permite retornar un objeto con los valores que queremos mostrar.
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }



class Films(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    episode_id = db.Column(db.String(250), nullable=True)
    opening_crawl = db.Column(db.String(250), nullable=True)
    director = db.Column(db.String(250), nullable=True)
    producer = db.Column(db.String(250), nullable=True)
    release_date = db.Column(db.String(250), nullable=True)
    created = db.Column(db.String(250), nullable=True)
    edited = db.Column(db.String(250), nullable=True)
    url = db.Column(db.String(250), nullable=True)
    # id_people = db.Column(db.Integer, db.ForeignKey('people.id'))
    # id_planets = db.Column(db.Integer, db.ForeignKey('planets.id'))
    # id_vehicles = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    # id_species = db.Column(db.Integer, db.ForeignKey('species.id'))
    # id_starships = db.Column(db.Integer, db.ForeignKey('starships.id'))

    # films_favorites = relationship('favorites', backref='films', lazy=True)
    # people = relationship('People', backref='films', lazy=True)
    # planets = relationship('Planets', backref='films', lazy=True)
    # vehicles = relationship('Vehicles', backref='films', lazy=True)
    # species = relationship('Species', backref='films', lazy=True)
    # starships = relationship('Starships', backref='films', lazy=True)

    def __repr__(self):
        return '<Films %r>' % self.id

    # Serialize permite retornar un objeto con los valores que queremos mostrar.
    def serialize(self):
        return {
            "id": self.id,
            "name": self.title,
            # do not serialize the password, its a security breach
        }    


class Starships(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    model = db.Column(db.String(250), nullable=True)
    starship_class = db.Column(db.String(250), nullable=True)
    manufacturer = db.Column(db.String(250), nullable=True)
    length = db.Column(db.String(250), nullable=True)
    cost_in_credits = db.Column(db.String(250), nullable=True)
    crew = db.Column(db.String(250), nullable=True)
    passengers = db.Column(db.String(250), nullable=True)
    max_atmosphering_speed = db.Column(db.String(250), nullable=True)
    hiper_drive_rating = db.Column(db.String(250), nullable=True)
    MGLT = db.Column(db.String(250), nullable=True)
    cargo_capacity = db.Column(db.String(250), nullable=True)
    consumables = db.Column(db.String(250), nullable=True)
    created = db.Column(db.String(250), nullable=True)
    edited = db.Column(db.String(250), nullable=True)
    url = db.Column(db.String(250), nullable=True)
    # id_people = db.Column(db.Integer, db.ForeignKey('people.id'))
    # id_films = db.Column(db.Integer, db.ForeignKey('films.id'))
    # starships_favorites = db.relationship('favorites', backref='starships', lazy=True)

    def __repr__(self):
        return '<Starships %r>' % self.id

    # Serialize permite retornar un objeto con los valores que queremos mostrar.
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    id_people = db.Column(db.Integer, db.ForeignKey('people.id'))
    id_vehicles = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    id_species = db.Column(db.Integer, db.ForeignKey('species.id'))
    # id_films = db.Column(db.Integer, db.ForeignKey('films.id'))
    id_starships = db.Column(db.Integer, db.ForeignKey('starships.id'))
    id_planets = db.Column(db.Integer, db.ForeignKey('planets.id'))


    def __repr__(self):
        return '<Favorites %r>' % self.id

    # Serialize permite retornar un objeto con los valores que queremos mostrar.
    # Creamos ifs para cada tipo de favorito(planet ,people...)
    def serialize(self):
        # Si en id_people de fav hay algo crearemos people y buscaremos en el mod people el id que tenemos como id_people
        if self.id_people is not None:
            people = People.query.filter_by(id=self.id_people).first()
            return{
                #devolveremos el id nuestro, el del usuario y la info de people serializada
                "id": self.id,
                "user": self.id_user,
                "info_people": people.serialize()
            }
        if self.id_planets is not None:
            planet = Planets.query.filter_by(id=self.id_planets).first()
            return{
                "id": self.id,
                "user": self.id_user,
                "info_planet": planet.serialize()
            }
        if self.id_vehicles is not None:
            vehicle = Vehicles.query.filter_by(id=self.id_vehicles).first()
            return{
                "id": self.id,
                "user": self.id_user,
                "info_vehicle": planet.serialize()
            }
        if self.id_species is not None:
            specie = Species.query.filter_by(id=self.id_species).first()
            return{
                "id": self.id,
                "user": self.id_user,
                "info_specie": specie.serialize()
            }
        if self.id_starships is not None:
            starship = Starships.query.filter_by(id=self.id_starships).first()
            return{
                "id": self.id,
                "user": self.id_user,
                "info_starship": starship.serialize()
            }
        return {
            "id": self.id,
            "user": self.id_user,
            "info_people": None if self.id_people is None else people.serialize(),
            "info_planet": None if self.id_planets is None else planet.serialize(),
            "info_vehicle": None if self.id_vehicles is None else vehicle.serialize(),
            "info_specie": None if self.id_species is None else specie.serialize(),
            "info_starship": None if self.id_starship is None else starship.serialize()
            # do not serialize the password, its a security breach
            # En el return general de favorites devolveremos el id, el user id y todas las info de todos los tipos
        }