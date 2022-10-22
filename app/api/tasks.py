from flask import jsonify, request, url_for, abort
from app import db
from app.models import Task
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request

@bp.route('/tasks/<string:id>', methods=['GET'])
@token_auth.login_required
def get_task(id):
    """
    Preliminary.  Users who are the owner of a task may access details about it.
    """
    the_task = Task.query.get_or_404(id)

    if token_auth.current_user().id == the_task.user_id:
        return jsonify(Task.query.get_or_404(id).to_dict())
    else:
        abort(403)

@bp.route('/tasks', methods=['GET'])
@token_auth.login_required
def get_tasks():
    """
    Preliminary.  Return all the tasks where the logged in user is the owner.
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Task.to_collection_dict(
        Task.query.filter(
            Task.user_id == token_auth.current_user().id),
        page, per_page, 'api.get_tasks')
    return jsonify(data)

@bp.route('/tasks', methods=['POST'])
@token_auth.login_required
def create_task():
    """
    Preliminary.  Allows a logged in user to create a task.
    """
    data = request.get_json() or {}
    if 'name' not in data or \
       'description' not in data or 'user_id' not in data:
        return \
            bad_request('must include name, description, and user_id fields')

    if token_auth.current_user().get_task_in_progress(data['name']):
        return bad_request('that task is already in progress')
    
    token_auth.current_user().launch_task(data['name'], data['description'])
    db.session.commit()
    task = token_auth.current_user().get_task_in_progress(data['name'])
    response = jsonify(task.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_task', id=task.id)
    return response
