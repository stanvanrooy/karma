from flask import Flask, g
from flask_cors import CORS

import routes

app = Flask(__name__)
CORS(app)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    routes.alert.initialize_routes(app)
    routes.note.initalize_routes(app)
    app.run(debug=False, host='localhost')

