from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config
import os


app = Flask(__name__)

CORS(app)
env = os.environ.get('FLASK_ENV', 'dev')
app.config.from_object(config[env])

db = SQLAlchemy(app)
db.create_all()
db.session.commit()

# import and register blueprints
from api.views import main
app.register_blueprint(main.mod)

from api.views import pois
app.register_blueprint(pois.mod)

from api.views import stories
app.register_blueprint(stories.mod)

from api.views import maps
app.register_blueprint(maps.mod)

from api.views import search
app.register_blueprint(search.mod)
