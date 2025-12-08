import os
from models.chicken_model import ChickenModel
from models.farm_model import FarmModel

# Initialize the models to create the database
chicken_model = ChickenModel()
farm_model = FarmModel()

print("Database initialized successfully!")