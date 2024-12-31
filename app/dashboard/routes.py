from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from . import bp

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """Dashboard home page"""
    try:
        return render_template('dashboard/index.html', user=current_user)
    except Exception as e:
        print(f"Error in dashboard index: {str(e)}")
        return redirect(url_for('auth.auth_start')) 