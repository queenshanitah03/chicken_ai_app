import os

# Configuration for the application
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chicken-farming-secret-key'
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'chicken_farm.db')
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models')