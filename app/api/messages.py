from flask import jsonify, request, url_for, abort
from app import db
from app.models import Message
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request

@bp.route('/messages/<int:id>', methods=['GET'])
@token_auth.login_required
def get_message(id):
    """
    Need to enforce only allowing the intended sender/recipient accessing the
    message.
    """
    return jsonify(Message.query.get_or_404(id).to_dict())

@bp.route('/messages', methods=['GET'])
@token_auth.login_required
def get_messages():
    """
    This needs to be modified to only return the messages for the logged in user
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Message.to_collection_dict(Message.query, page, per_page, 'api.get_messages')
    return jsonify(data)

@bp.route('/messages', methods=['POST'])
@token_auth.login_required
def create_message():
    data = request.get_json() or {}
    if 'body' not in data \
       or 'sender_id' not in data or 'recipient_id' not in data:
        return bad_request('must include body and user_id fields')
    message = Message()
    message.from_dict(data)

    db.session.add(message)
    db.session.commit()
    response = jsonify(message.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_message', id=message.id)
    return response

