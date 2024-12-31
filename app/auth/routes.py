from flask import Blueprint, render_template, redirect, url_for, session, request, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import msal
from app.models import User
from app import db
import traceback
from . import bp

@bp.route('/auth-start')
def auth_start():
    """Show the login page"""
    try:
        # If user is already authenticated, redirect to dashboard
        if current_user.is_authenticated:
            print(f"User {current_user.email} is already authenticated, redirecting to dashboard")
            return redirect(url_for('dashboard.index'))
        
        # Show login page for non-authenticated users
        print("Showing login page for non-authenticated user")
        return render_template('auth/login.html')
    except Exception as e:
        print(f"Error in auth_start: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/callback', methods=['GET', 'POST'])
def callback():
    try:
        if request.method == 'POST':
            print("Received POST request to /callback")
            
            try:
                data = request.get_json()
                print("Received callback data:", data)
            except Exception as e:
                print(f"Error parsing JSON: {str(e)}")
                return jsonify({'error': 'Invalid JSON data'}), 400
            
            if not data:
                print("No data provided in request")
                return jsonify({'error': 'No data provided'}), 400
            
            account_info = data.get('account')
            print("Account info:", account_info)
            
            if not account_info:
                print("No account info provided")
                return jsonify({'error': 'No account info provided'}), 400
            
            # Get user info from account
            email = account_info.get('username')
            name = account_info.get('name', email)
            
            print(f"Extracted email: {email}, name: {name}")
            
            if not email:
                print("No email provided in account info")
                return jsonify({'error': 'No email provided'}), 400
            
            try:
                # Create or update user
                user = User.query.filter_by(email=email).first()
                if not user:
                    print(f"Creating new user: {email}")
                    user = User(email=email, name=name)
                    db.session.add(user)
                elif user.name != name:
                    print(f"Updating user name from {user.name} to {name}")
                    user.name = name
                
                db.session.commit()
                print(f"Database operations successful for user: {email}")
                
                login_user(user, remember=True)
                print(f"User logged in successfully: {email}")
                
                # Store user info in session
                session['user_email'] = email
                session['user_name'] = name
                
                response_data = {
                    'success': True,
                    'redirect': url_for('dashboard.index'),
                    'message': 'Successfully logged in'
                }
                print("Sending response:", response_data)
                return jsonify(response_data)
            
            except Exception as e:
                db.session.rollback()
                print(f"Database error: {str(e)}")
                print(traceback.format_exc())
                return jsonify({'error': f'Database error: {str(e)}'}), 500
            
        # Handle GET request - redirect to dashboard if already authenticated
        if current_user.is_authenticated:
            print(f"User {current_user.email} is already authenticated, redirecting to dashboard")
            return redirect(url_for('dashboard.index'))
            
        print("Received GET request to /callback")
        return redirect(url_for('auth.auth_start'))

    except Exception as e:
        print(f"Unhandled error in callback: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    try:
        # Get user info before logout for logging
        user_email = current_user.email if current_user else 'Unknown'
        
        # Clear Flask-Login session
        logout_user()
        
        # Clear Flask session
        session.clear()
        
        print(f"User {user_email} logged out successfully")
        
        # Return JSON response for AJAX call
        return jsonify({
            'success': True,
            'redirect': url_for('auth.auth_start'),
            'message': 'Successfully logged out'
        })
        
    except Exception as e:
        print(f"Error in logout: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': 'Logout failed',
            'redirect': url_for('auth.auth_start')
        }), 500 