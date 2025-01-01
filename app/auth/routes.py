from flask import Blueprint, render_template, redirect, url_for, session, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_oidc import OpenIDConnect
from app.models import User
from app import db, oidc
from . import bp

@bp.route('/login')
def login():
    """Show login page or redirect to Azure AD"""
    if oidc.user_loggedin:
        return redirect(url_for('dashboard.index'))
    return render_template('auth/login.html')

@bp.route('/callback')
@oidc.require_login
def callback():
    """Handle the Azure AD callback"""
    try:
        # Get user info from Azure AD
        user_info = oidc.user_getinfo(['preferred_username', 'name', 'email'])
        email = user_info.get('preferred_username') or user_info.get('email')
        name = user_info.get('name', email)

        if not email:
            return jsonify({'error': 'No email provided'}), 400

        # Create or update user
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, name=name)
            db.session.add(user)
        elif user.name != name:
            user.name = name
        
        db.session.commit()

        # Log user in
        login_user(user)
        
        # Store user info in session
        session['user_email'] = email
        session['user_name'] = name
        
        return redirect(url_for('dashboard.index'))
        
    except Exception as e:
        current_app.logger.error(f"Error in callback: {str(e)}")
        return jsonify({'error': 'Authentication failed'}), 500

@bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    try:
        # Clear Flask-Login
        logout_user()
        
        # Clear Flask session
        session.clear()
        
        # Redirect to Azure AD logout
        return redirect(oidc.logout_url)
        
    except Exception as e:
        current_app.logger.error(f"Error in logout: {str(e)}")
        return redirect(url_for('auth.login')) 