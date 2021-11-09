from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'djfaksldjfaksdjfkajsdfjaslkfjk'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)



from .views import views
from .auth import auth

from .models import User,Note


app.register_blueprint(views, url_Prefix='/')
app.register_blueprint(auth, url_Prefix='/')

def create_database(app):
    if not path.exists('Notes/'+ DB_NAME):
        db.create_all(app=app)
        print('Database Created!!') 

create_database(app)
    
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'danger'
login_manager.login_message = 'Please Login To Access This Page.'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))