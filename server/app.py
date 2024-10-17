from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db, bcrypt
from routes import api_blueprint
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

jwt = JWTManager(app)
CORS(app)

app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
