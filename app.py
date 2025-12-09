import os
import sys
from backend.app import app

def setup_database():
    """Initialize the database by importing the models"""
    from models.chicken_model import ChickenModel
    from models.farm_model import FarmModel
    
    print("Initializing database...")
    chicken_model = ChickenModel()
    farm_model = FarmModel()
    print("Database initialized successfully!")

if __name__ == '__main__':
    # Create the database if it doesn't exist
    setup_database()
    
    print("Starting Chicken Farming AI App...")
    print("Visit http://localhost:5000 to access the application")
    app.run(debug=True, host='0.0.0.0', port=5000)
