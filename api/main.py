from flask import Flask
from flask_cors import CORS
import database
import config

import routes

app = Flask(__name__)
CORS(app)
config.init_app(app)


database.db.init_app(app)
with app.app_context():
    database.db.create_all()
routes.alert.initialize_routes(app)
routes.note.initalize_routes(app)

