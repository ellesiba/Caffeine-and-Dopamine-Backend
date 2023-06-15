from flask import Flask, g, request, jsonify
from flask_cors import CORS

import models
from resources.secretmenu import menu

DEBUG = True
PORT = 8000

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'], supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE'], allow_headers=['Content-Type'])
app.register_blueprint(menu, url_prefix='/api/v1/secret_menu')

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    g.db.close()
    return response

# Health Check
@app.route('/')
def index():
    return 'Service is alive!!'

# Custom OPTIONS route for handling preflight requests
@app.route('/api/v1/secret_menu', methods=['OPTIONS'])
def handle_options_request():
    """Handle OPTIONS request explicitly."""
    response = jsonify()
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Max-Age'] = 3600
    return response

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
