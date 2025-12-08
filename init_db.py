from app import app
from extensions import db

# Ensure this runs within the Flask application context
with app.app_context():
    # Create all tables defined in your models
    db.create_all()
    print("Database tables created successfully!")
