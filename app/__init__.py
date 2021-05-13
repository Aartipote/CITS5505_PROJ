from flask import Flask,  render_template
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdjfdfij'

# ----------------------------------------------
rootdir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(rootdir + 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# passing the app to the sqlalchemy
db = SQLAlchemy(app)
# ----------------------------------------------

from app import views