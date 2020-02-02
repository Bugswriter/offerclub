#bugswriter/ main package initialization
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hungrynigga.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config['SECRET_KEY'] = "9be8f28f87c515b14ea6bf8a647fdcf5"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'akashraj5399@gmail.com'
app.config['MAIL_PASSWORD'] = 'vgdvirbrjdlakbky'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)
mail = Mail(app)

from hungrynigga.admin.routes import admin
from hungrynigga.main.routes import main
from hungrynigga.users.routes import users
from hungrynigga.items.routes import items
from hungrynigga.orders.routes import orders
from hungrynigga.errors.handlers import errors

app.register_blueprint(admin)
app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(items)
app.register_blueprint(orders)
app.register_blueprint(errors)

