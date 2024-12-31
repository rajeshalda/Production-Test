from flask import Blueprint, render_template, redirect, url_for, session, request, current_app, jsonify
from flask_login import login_user, logout_user, login_required
import msal
from app.models import User
from app import db
from . import bp

@bp.route('/auth-start')
def auth_start():
    """Show the login page"""
    return render_template('auth/login.html')

@bp.route('/callback', methods=['GET', 'POST'])
def callback():
    try:
        if request.method == 'POST':
            # Handle popup authentication
            data = request.get_json()
            if not data or 'token' not in data:
                return jsonify({'error': 'No token provided'}), 400
            
            access_token = data['token']
            account_info = data.get('account', {})
            
            # Get user info from account
            email = account_info.get('username', '')
            name = account_info.get('name', email)
            
        else:
            # Handle redirect authentication
            auth_code = request.args.get('code')
            if not auth_code:
                return redirect(url_for('auth.auth_start'))

            msal_app = msal.PublicClientApplication(
                client_id=current_app.config['MICROSOFT_CLIENT_ID'],
                authority=current_app.config['MICROSOFT_AUTHORITY']
            )

            result = msal_app.acquire_token_by_authorization_code(
                code=auth_code,
                scopes=current_app.config['SCOPE'],
                redirect_uri=url_for('auth.callback', _external=True)
            )

            if "error" in result:
                print(f"Error in token acquisition: {result.get('error_description', 'Unknown error')}")
                return redirect(url_for('auth.auth_start'))

            if "access_token" not in result:
                return redirect(url_for('auth.auth_start'))

            access_token = result['access_token']
            id_claims = result.get('id_token_claims', {})
            email = id_claims.get('preferred_username', '')
            name = id_claims.get('name', email)

        # Store token in session
        session['access_token'] = access_token
        
        # Create or update user
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, name=name)
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
        
        if request.method == 'POST':
            return jsonify({'success': True, 'redirect': url_for('dashboard.index')})
        return redirect(url_for('dashboard.index'))

    except Exception as e:
        print(f"Error in callback: {str(e)}")
        if request.method == 'POST':
            return jsonify({'error': str(e)}), 500
        return redirect(url_for('auth.auth_start'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.auth_start')) 