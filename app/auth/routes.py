from flask import Blueprint, render_template, redirect, url_for, session, request, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import msal
from app.models import User
from app import db
from . import bp

@bp.route('/auth-start')
def auth_start():
    """Show the login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('auth/login.html')

@bp.route('/callback', methods=['GET', 'POST'])
def callback():
    try:
        if request.method == 'POST':
            data = request.get_json()
            print("Received callback data:", data)  # Debug log
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            account_info = data.get('account')
            if not account_info:
                return jsonify({'error': 'No account info provided'}), 400
            
            # Get user info from account
            email = account_info.get('username')
            name = account_info.get('name', email)
            
            if not email:
                return jsonify({'error': 'No email provided'}), 400
            
            print(f"Processing user: {email}, {name}")  # Debug log
            
            try:
                # Create or update user
                user = User.query.filter_by(email=email).first()
                if not user:
                    print(f"Creating new user: {email}")  # Debug log
                    user = User(email=email, name=name)
                    db.session.add(user)
                elif user.name != name:
                    print(f"Updating user name: {name}")  # Debug log
                    user.name = name
                
                db.session.commit()
                login_user(user, remember=True)
                
                print(f"User logged in successfully: {email}")  # Debug log
                return jsonify({
                    'success': True,
                    'redirect': url_for('dashboard.index'),
                    'message': 'Successfully logged in'
                })
            
            except Exception as e:
                db.session.rollback()
                print(f"Database error: {str(e)}")
                return jsonify({'error': f'Database error: {str(e)}'}), 500
            
        # Handle GET request
        return redirect(url_for('auth.auth_start'))

    except Exception as e:
        print(f"Error in callback: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.auth_start')) 