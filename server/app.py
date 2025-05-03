from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt
from models import Hotel, User, Room, Booking
import os

def init_database(app):
    """Initialize database and verify connection"""
    db_path = os.path.join(os.path.dirname(app.root_path), 'database', 'innstayDB.sqlite')
    
    if not os.path.exists(db_path):
        print(f"⚠️ Database file not found at: {db_path}")
        return False
    
    try:
        with app.app_context():
            hotels_count = db.session.query(db.func.count(Hotel.id)).scalar()
            print(f"✅ Connected to SQLite database")
            print(f"📊 Found {hotels_count} hotels")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Initialize database connection
    if not init_database(app):
        raise Exception("Failed to initialize database")
    
    # Register blueprints
    from routes.hotels import hotels_bp
    app.register_blueprint(hotels_bp, url_prefix="/api/hotels")

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)