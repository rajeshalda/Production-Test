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
    
    # Azure OpenAI Config
    AZURE_OPENAI_KEY = "CWDspACTbjoETrgOOAi7i2cGXJiHRrFEg6ZciiqxXdy3u9aIWcuSJQQJ99ALACYeBjFXJ3w3AAABACOGQTIv"
    AZURE_OPENAI_ENDPOINT = "https://rajesh-azure-open-ai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"
    
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

    # Deployment settings
    DEPLOYMENT_ENV = os.environ.get('DEPLOYMENT_ENV', 'development')
    
    # For local development
    if DEPLOYMENT_ENV == 'development':
        SERVER_NAME = "127.0.0.1:5001"
    else:
        # For Azure App Service
        SERVER_NAME = os.environ.get('WEBSITE_HOSTNAME')  # Azure App Service provides this
    
    # MSAL Config
    MICROSOFT_REDIRECT_PATH = '/auth/callback'
    
    # Azure OpenAI Config
    AZURE_OPENAI_KEY = "CWDspACTbjoETrgOOAi7i2cGXJiHRrFEg6ZciiqxXdy3u9aIWcuSJQQJ99ALACYeBjFXJ3w3AAABACOGQTIv"
    AZURE_OPENAI_ENDPOINT = "https://rajesh-azure-open-ai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"
    
    # Microsoft Graph API Scopes
    SCOPE = [
        "https://graph.microsoft.com/Calendars.Read",
        "https://graph.microsoft.com/User.Read",
        "https://graph.microsoft.com/OnlineMeetings.Read"
    ] 