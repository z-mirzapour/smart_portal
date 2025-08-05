import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'smartportalproject123'
    DATA_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))