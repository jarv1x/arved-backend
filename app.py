from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from routes.auth import auth_bp
    from routes.invoices import invoices_bp
    from routes.readings import readings_bp
    from routes.payments import payments_bp
    from routes.balance import balance_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(invoices_bp, url_prefix="/invoices")
    app.register_blueprint(readings_bp, url_prefix="/readings")
    app.register_blueprint(payments_bp, url_prefix="/payments")
    app.register_blueprint(balance_bp, url_prefix="/balance")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
