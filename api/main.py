from flask import Flask
from flask_cors import CORS
import database
import config
import auth
import logging
logging.basicConfig(level=logging.DEBUG)

import routes

def create_app(testing=False):
    app = Flask(__name__)
    app.secret_key = 'secret'
    app.register_blueprint(routes.alert.a, url_prefix='/api/1/alert')
    app.register_blueprint(routes.note.n, url_prefix='/api/1/note')
    app.register_blueprint(routes.auth.a, url_prefix='/api/1/auth')
    app.register_blueprint(routes.webhook.w, url_prefix='/api/1/webhook')

    CORS(app)
    config.init_app(app, testing)

    database.db.init_app(app)
    with app.app_context():
        database.db.create_all()
        admin = database.db.session.query(database.User).filter(database.User.username == 'admin').first()
        if admin is None:
            c = config.get_config()
            database.db.session.add(database.User(
                username='admin',
                password=auth.hash_password(c.admin.password)
            ))
            database.db.session.commit()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

