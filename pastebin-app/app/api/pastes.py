import ast
from datetime import datetime, timedelta
from flasgger import swag_from
from flask import current_app, request, abort
from flask import send_from_directory, jsonify
from app.main.url_service import generate_shortlink
from app.models import User, Paste, Tag
from app.api import bp
import sqlalchemy
from app.api.auth import token_auth
from app.api.errors import bad_request
import json
import os
from app import db


@bp.route('/pastes/<shortlink>', methods=['GET'])
@swag_from('docs/view_paste.yml')
def view_paste(shortlink):
    """
    view the paste content
    """
    return send_from_directory(current_app.config['PASTES_FOLDER'], f"{shortlink}.txt"), 200


@bp.route('/paste/new', methods=['POST'])
@token_auth.login_required
@swag_from('docs/new_paste.yml')
def new_paste():
    """
    create a new paste
    """
    if token_auth.current_user().pastes.count() >= current_app.config['USER_PASTES_LIMIT']:
        abort(400)
    data = request.get_json() or {}
    if 'content' not in data or 'tags' not in data or 'expires' not in data:
        return bad_request('must include content, tags and expires fields')
    if len(data['content']) == 0:
        return bad_request('content cannot be empty')
    if any(len(tag) > 16 for tag in ast.literal_eval(data['tags'])):
        return bad_request('tags cannot exceed 16 characters in length')
    if data['expires'] not in ['Never' , '1 Hour', '1 Day', '1 Week']:
        return bad_request("expires must be 'Never', '1 Hour', '1 Day' or '1 Week'")
    # add tags to database
    for tag in ast.literal_eval(data['tags']):
        if not Tag.query.filter_by(value=tag).first():
            tag_record = Tag(value=tag)
            db.session.add(tag_record)
            db.session.commit()
    shortlink = generate_shortlink(
        request.remote_addr, str(datetime.utcnow()), 8)
    created_at = datetime.utcnow()
    expires_at = created_at + timedelta(hours=1) if data['expires'] == '1 Hour' else \
        created_at + timedelta(days=1) if data['expires'] == '1 Day' else \
        created_at + timedelta(weeks=1) if data['expires'] == '1 Week' else \
        sqlalchemy.null()
    paste_path = f"{current_app.config['PASTES_FOLDER']}/{shortlink}.txt"
    user_id = token_auth.current_user().id
    json_metadata = json.dumps({"tags": ast.literal_eval(data['tags'])})
    # write data to file
    with open(paste_path, 'w') as f:
        f.write(data['content'])
    # add paste to database
    paste = Paste(shortlink=shortlink, created_at=created_at, expires_at=expires_at,
                  paste_path=paste_path, user_id=user_id, json_metadata=json_metadata)
    db.session.add(paste)
    db.session.commit()
    return 'Paste created successfully!', 201


@bp.route('/delete/<shortlink>', methods=['DELETE'])
@token_auth.login_required
@swag_from('docs/delete_paste.yml')
def delete_paste(shortlink):
    """
    delete the paste and the file
    """
    paste = Paste.query.filter_by(shortlink=shortlink)
    if paste.one_or_none() is None:
        abort(400)
    if paste.one_or_none().user_id != token_auth.current_user().id:
        abort(403)
    paste.delete()
    db.session.commit()
    try:
        os.remove(f"{current_app.config['PASTES_FOLDER']}/{shortlink}.txt")
    except:
        pass
    return 'Deleted paste sucessfully!', 200


@bp.route('/pastes/expired', methods=['GET'])
def expired_pastes():
    """
    return the expired pastes
    no authorization needed
    """
    pastes = Paste.query.filter(Paste.expires_at < datetime.utcnow()).all()
    return jsonify({"pastes": [{"shortlink": paste.shortlink} for paste in pastes]}), 200


@bp.route('/delete_expired/<shortlink>', methods=['DELETE'])
def delete_expired(shortlink):
    """
    delete the paste if is has expired
    no authorization needed
    """
    paste = Paste.query.filter_by(shortlink=shortlink)
    if paste.one_or_none() is None:
        abort(400)
    paste.delete()
    db.session.commit()
    try:
        os.remove(f"{current_app.config['PASTES_FOLDER']}/{shortlink}.txt")
    except:
        pass
    return 'Deleted paste sucessfully!', 200
