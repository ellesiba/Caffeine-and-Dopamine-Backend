# from flask import Flask, g
# from flask_cors import CORS

# import models
# from resources.secretmenu import menu

# DEBUG = True
# PORT = 8000

# app = Flask(__name__)

# @app.before_request
# def before_request():
#     """Connect to the database before each request."""
#     g.db = models.DATABASE
#     g.db.connect()


# @app.after_request
# def after_request(response):
#     """Close the database connection after each request."""
#     g.db.close()
#     return response


# CORS(menu, origins=['http://localhost:3000'], supports_credentials=True) 
# app.register_blueprint(menu, url_prefix='/api/v1/secret_menu') 

# # Health Check
# @app.route('/')
# def index():
#     return 'Service is alive!!'



# if __name__ == '__main__':
#     models.initialize()
#     app.run(debug=DEBUG, port=PORT)

from flask import Flask, g, jsonify
from flask_cors import CORS
import logging
import models
from resources.secretmenu import menu

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'  # Set the CORS headers

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

CORS(app)  # Apply CORS to the entire app

app.register_blueprint(menu, url_prefix='/api/v1/secret_menu')

# Health Check
@app.route('/')
def index():
    return 'Service is alive!!'

# Example endpoint for retrieving menu items
@app.route('/api/v1/secret_menu/items', methods=['GET'])
def get_menu_items():
    try:
        items = models.MenuItem.select().dicts()
        return jsonify(list(items))
    except Exception as e:
        logging.error("Error retrieving menu items: %s", str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)  # Enable logging for errors
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
