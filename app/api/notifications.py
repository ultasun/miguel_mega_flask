from flask import jsonify, request, url_for, abort
from app import db
from app.models import Notification
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request

@bp.route('/notifications/<int:id>', methods=['GET'])
@token_auth.login_required
def get_notification(id):
    """
    Preliminary.  Users who are the owner of a notification may access a
    notification by the id.
    """
    the_notification = Notification.query.get_or_404(id)

    if token_auth.current_user().id == the_notification.user_id:
        return jsonify(Notification.query.get_or_404(id).to_dict())
    else:
        abort(403)

@bp.route('/notifications', methods=['GET'])
@token_auth.login_required
def get_notifications():
    """
    Preliminary.  Return all the notifications where the logged in user is the
    owner.
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Notification.to_collection_dict(
        Notification.query.filter(
            Notification.user_id == token_auth.current_user().id),
        page, per_page, 'api.get_notifications')
    return jsonify(data)

# there seems no use case where it would be applicable to allow a client
# to manually POST a new notification 
