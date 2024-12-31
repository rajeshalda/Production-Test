from flask import jsonify
from . import bp

@bp.route('/sync', methods=['POST'])
def sync():
    return jsonify({'status': 'success'})

@bp.route('/meetings/<int:meeting_id>/match', methods=['POST'])
def match_meeting(meeting_id):
    return jsonify({'status': 'success', 'meeting_id': meeting_id})

@bp.route('/meetings/post-all', methods=['POST'])
def post_all_meetings():
    return jsonify({'status': 'success'}) 