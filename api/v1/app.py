#!/usr/bin/python3
"""API entry point"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def close_storage(exception):
    """Close the storage"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with JSON response"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    from os import getenv
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
