from dotenv import load_dotenv
from environs import Env

load_dotenv()
env = Env()

class Config:
    """Set Flask config variables."""
    FLASK_APP = 'start.py'

    FLASK_DEBUG = env.bool('FLASK_DEBUG')
    TESTING = env.bool('FLASK_TESTING')
    
    BASIC_AUTH_USERNAME = env('BASIC_AUTH_USERNAME')
    BASIC_AUTH_PASSWORD = env('BASIC_AUTH_PASSWORD')

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    SCHEDULER_API_ENABLED = True

    import secrets
    SECRET_KEY = secrets.token_hex(64)
