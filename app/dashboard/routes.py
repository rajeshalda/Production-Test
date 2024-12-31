from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    # Mock data for demonstration
    unmatched_meetings = [{
        'id': 1,
        'title': 'Technical Discussion',
        'description': 'Architecture review meeting',
        'duration': '1.5 hours',
        'datetime': '2024-12-24 10:00 AM'
    }]
    
    matched_meetings = [{
        'id': 2,
        'title': 'Sprint Planning',
        'description': 'Weekly sprint planning session',
        'duration': '1 hour',
        'task': 'Sprint Planning',
        'project': 'Project Alpha',
        'datetime': '2024-12-24 2:00 PM'
    }]
    
    return render_template('dashboard/index.html',
                         unmatched_meetings=unmatched_meetings,
                         matched_meetings=matched_meetings)

@bp.route('/meetings')
@login_required
def meetings():
    """Meetings list page."""
    return render_template('dashboard/meetings.html')

@bp.route('/tasks')
@login_required
def tasks():
    """Tasks list page."""
    return render_template('dashboard/tasks.html') 