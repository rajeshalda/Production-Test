from flask import Blueprint, render_template, redirect, url_for, session, request, current_app
from flask_login import login_user, logout_user, login_required
import msal
from app.models import User
from app import db
from . import bp

@bp.route('/login')
def login():
    # Generate Microsoft login URL
    msal_app = msal.PublicClientApplication(
        client_id=current_app.config['MICROSOFT_CLIENT_ID'],
        authority=current_app.config['MICROSOFT_AUTHORITY']
    )
    
    auth_url = msal_app.get_authorization_request_url(
        scopes=current_app.config['SCOPE'],
        redirect_uri=url_for('auth.callback', _external=True),
        prompt="select_account",
        response_type="code"
    )
    
    return redirect(auth_url)

@bp.route('/auth-start')
def auth_start():
    """Show the login page"""
    return render_template('auth/login.html')

@bp.route('/callback')
def callback():
    try:
        # Get the authorization code from the URL
        auth_code = request.args.get('code')
        if not auth_code:
            return redirect(url_for('auth.auth_start'))

        # Initialize MSAL application
        msal_app = msal.PublicClientApplication(
            client_id=current_app.config['MICROSOFT_CLIENT_ID'],
            authority=current_app.config['MICROSOFT_AUTHORITY']
        )

        # Acquire token using authorization code
        result = msal_app.acquire_token_by_authorization_code(
            code=auth_code,
            scopes=current_app.config['SCOPE'],
            redirect_uri=url_for('auth.callback', _external=True)
        )

        if "error" in result:
            print(f"Error in token acquisition: {result.get('error_description', 'Unknown error')}")
            return redirect(url_for('auth.auth_start'))

        # Get user info from the token
        if "access_token" in result:
            # Store token in session
            session['access_token'] = result['access_token']
            
            # Get user info from ID token claims
            id_claims = result.get('id_token_claims', {})
            email = id_claims.get('preferred_username', '')
            name = id_claims.get('name', email)
            
            # Create or update user
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(email=email, name=name)
                db.session.add(user)
                db.session.commit()
            
            login_user(user)
            return redirect(url_for('dashboard.index'))

        return redirect(url_for('auth.auth_start'))
    except Exception as e:
        print(f"Error in callback: {str(e)}")
        return redirect(url_for('auth.auth_start'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.auth_start')) 