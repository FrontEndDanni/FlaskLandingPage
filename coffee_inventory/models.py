from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime


#Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

#Import for Secretes Module (given by python)
import secrets

#Imports for Flask_login
from flask_login import UserMixin, LoginManager

#Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = "")
    last_name = db.Column(db.String(150), nullable = True, default = "")
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = "")
    token = db.Column(db.String, default = "", unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name = "", last_name = "", id = "", password =  "", token = ""):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email 
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"User {self.email} has been added to the database."

class Coffee(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    caffeine_level = db.Column(db.String(150), nullable = True)
    price = db.Column(db.Numeric(precision=10, scale=2))
    roast = db.Column(db.String(200), nullable = True)
    cost_of_production = db.Column(db.Numeric(precision=10, scale=2))
    place_of_origin = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, name, description, caffeine_level, price, roast, cost_of_production, place_of_origin, user_token, id = ""):
        self.id = self.set_id()
        self.name = name
        self.description = description 
        self.caffeine_level = caffeine_level
        self.price = price
        self.roast = roast
        self.cost_of_production = cost_of_production 
        self.place_of_origin = place_of_origin
        self.user_token = user_token

    def __repr__(self):
        return f"The following coffee has been added: {self.name}"

    def set_id(self):
        return(secrets.token_urlsafe())

#Creation of API Schema via the Marshmallow Object
class CoffeeSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'caffeine_level', 'price', 'roast', 'cost_of_production', 'place_of_origin']

coffee_schema = CoffeeSchema()
coffees_schema = CoffeeSchema(many = True)