import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Azure AD configuration
    AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID')
    AZURE_TENANT_ID = os.environ.get('AZURE_TENANT_ID')
    AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
    
    # OIDC Configuration
    OIDC_CLIENT_SECRETS = {
        "web": {
            "client_id": AZURE_CLIENT_ID,
            "client_secret": AZURE_CLIENT_SECRET,
            "auth_uri": f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/authorize",
            "token_uri": f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/token",
            "userinfo_uri": "https://graph.microsoft.com/oidc/userinfo",
            "issuer": f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0",
            "redirect_uris": [
                os.environ.get('REDIRECT_URI', 'http://localhost:5001/auth/callback')
            ]
        }
    }
    OIDC_ID_TOKEN_COOKIE_SECURE = False  # Set to True in production
    OIDC_REQUIRE_VERIFIED_EMAIL = False
    OIDC_USER_INFO_ENABLED = True
    OIDC_OPENID_REALM = os.environ.get('SERVER_NAME', 'localhost:5001')
    OIDC_SCOPES = ['openid', 'email', 'profile']
    OIDC_INTROSPECTION_AUTH_METHOD = 'client_secret_post'
    
    # Application configuration
    SERVER_NAME = os.environ.get('SERVER_NAME')
    PREFERRED_URL_SCHEME = 'https' 