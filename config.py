import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Azure AD configuration
    AZURE_CLIENT_ID = "9ec41cd0-ae8c-4dd5-bc84-a3aeea4bda54"
    AZURE_TENANT_ID = "a5ae9ae1-3c47-4b70-b92c-ac3a0efffc6a"
    AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
    AZURE_AUTHORITY = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    AZURE_REDIRECT_PATH = "/auth/callback"
    
    # Application configuration
    SERVER_NAME = os.environ.get('SERVER_NAME') or 'production-test-ggd3cccmbgg7f6hd.centralindia-01.azurewebsites.net'
    PREFERRED_URL_SCHEME = 'https' 