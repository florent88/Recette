from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


import Recette.views
import Recette.models

