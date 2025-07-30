import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from routes.auth import auth_bp
from routes.invoices import invoices_bp
from routes.readings import readings_bp
from routes.apartments import apartments_bp  # UUS IMPORT

app = Flask(__name__)

# ✅ Andmebaasi ühendus MySQL (või fallback SQLite)
# Näiteks: mysql+pymysql://root:root@db:3306/arved
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///app.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'supersecret')

# ✅ Initsialiseeri
db.init_app(app)
CORS(app)
jwt = JWTManager(app)

# ✅ Globaalne error handler
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': str(e)}), 500

# ✅ Blueprintid
app.register_blueprint(auth_bp)
app.register_blueprint(invoices_bp)
app.register_blueprint(readings_bp)
app.register_blueprint(apartments_bp)  # SIIN LISATUD

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
