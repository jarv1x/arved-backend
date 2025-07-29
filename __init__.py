from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Lubame CORS-i
    CORS(app)

    # Init DB
    db.init_app(app)

    # Registreeri route blueprintid
    from routes.auth import auth_bp
    from routes.invoices import invoices_bp
    from routes.payments import payments_bp
    from routes.balance import balance_bp
    from routes.readings import readings_bp
    from routes.apartments import apartments_bp

    app.register_blueprint(apartments_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(invoices_bp, url_prefix="/invoices")
    app.register_blueprint(payments_bp, url_prefix="/payments")
    app.register_blueprint(balance_bp, url_prefix="/balance")
    app.register_blueprint(readings_bp, url_prefix="/readings")


    # Loo tabelid ja lisa admin, kui ei ole olemas
    with app.app_context():
        from models import User
        db.create_all()
        create_default_admin()

    return app


def create_default_admin():
    """Loob vaikimisi admin kasutaja, kui teda pole."""
    from models import User
    if not User.query.filter_by(email="admin@demo.com").first():
        admin = User(email="admin@demo.com")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
