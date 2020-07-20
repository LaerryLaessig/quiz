import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

USER_ADMIN = os.getenv('USER_ADMIN')
PWD_ADMIN = os.getenv('PWD_ADMIN')

IMAGE_FOLDER = os.path.join('flask_quiz', 'static', 'images')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.add_url_rule('/static/images/<path:filename>',
                 endpoint='images',
                 view_func=app.send_static_file)

Bootstrap(app)

db = SQLAlchemy(app)

from flask_quiz import database
from flask_quiz import models
from flask_quiz import routes

database.create_database()
