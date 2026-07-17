"""
    Main Flask application for the backend 
    of the MiCartera project.    
"""
from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.cotizaciones import cotizaciones_bp
from routes.cartera import cartera_bp 

app = Flask(__name__)
CORS(app)

# Registro de blueprints
app.register_blueprint(auth_bp,          url_prefix='/api')
app.register_blueprint(cotizaciones_bp,  url_prefix='/api')
app.register_blueprint(cartera_bp,       url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)