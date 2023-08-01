from flask import Flask
from views import main_bp
import CloudFlare
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    cf = CloudFlare.CloudFlare()
    CORS(app)
    
    app.register_blueprint(main_bp)

    return app