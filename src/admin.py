import os
from flask_admin import Admin
# Deberemos importar las tablas que queremos que aparezcan
from models import db, User, People, Planets, Vehicles, Species, Films, Starships, Favorites
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    # Aquí en cada linea crearemos una por tabla
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(Vehicles, db.session))
    admin.add_view(ModelView(Species, db.session))
    admin.add_view(ModelView(Films, db.session))
    admin.add_view(ModelView(Starships, db.session))
    admin.add_view(ModelView(Favorites, db.session))



    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))


