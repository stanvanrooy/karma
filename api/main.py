from flask import Flask
from flask_cors import CORS
import database
import config

import routes

app = Flask(__name__)
app.register_blueprint(routes.alert.a, url_prefix='/api/alert')
app.register_blueprint(routes.note.n, url_prefix='/api/note')

CORS(app)
config.init_app(app)


database.db.init_app(app)
with app.app_context():
    database.db.create_all()
    admin = database.db.session.query(database.User).filter(database.User.username == 'admin').first()
    if admin is None:
        config = config.get_config()
        database.db.session.add(database.User(username='admin', password=config.admin.password))
        database.db.session.commit()


