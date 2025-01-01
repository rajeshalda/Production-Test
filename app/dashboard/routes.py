from flask import render_template, redirect, url_for, session
from flask_login import login_required, current_user
import traceback
from . import bp

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """Dashboard home page"""
    try:
        # Double check authentication
        if not current_user.is_authenticated:
            print("User not authenticated, redirecting to login")
            return redirect(url_for('auth.auth_start'))
            
        # Check session validity
        if 'user_email' not in session:
            print("Session expired, redirecting to login")
            return redirect(url_for('auth.auth_start'))
            
        print(f"Rendering dashboard for user: {current_user.email}")
        return render_template('dashboard/index.html', user=current_user)
    except Exception as e:
        print(f"Error in dashboard index: {str(e)}")
        print(traceback.format_exc())
        return redirect(url_for('auth.auth_start')) 