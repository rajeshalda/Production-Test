import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MSAL Config
    MICROSOFT_CLIENT_ID = "9ec41cd0-ae8c-4dd5-bc84-a3aeea4bda54"
    MICROSOFT_TENANT_ID = "a5ae9ae1-3c47-4b70-b92c-ac3a0efffc6a"
    MICROSOFT_AUTHORITY = f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}"
    
    # Deployment settings
    DEPLOYMENT_ENV = os.environ.get('DEPLOYMENT_ENV', 'development')
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    
    # Microsoft Graph API Scopes
    SCOPE = [
        "https://graph.microsoft.com/Calendars.Read",
        "https://graph.microsoft.com/User.Read",
        "https://graph.microsoft.com/OnlineMeetings.Read",
        "offline_access",
        "openid",
        "profile",
        "email"
    ] 