import json
import os
from datetime import datetime, timedelta
from werkzeug.urls import url_parse
from flask import render_template, request, current_app, redirect, url_for, flash, abort
from flask import send_from_directory, jsonify
from flask_login import login_required, current_user
import sqlalchemy
from app.main.forms import PasteForm
from app.main.url_service import generate_shortlink
from app.main import bp
from app.models import User, Paste, Tag
from app import db


def parse_tags(json_metadata):
    metadata = json.loads(json_metadata)
    return metadata["tags"]


def get_preview(shortlink):
    paste_file = f"{current_app.config['PASTES_FOLDER']}/{shortlink}.txt"
    if not os.path.exists(paste_file):
        return "No preview available"
    with open(paste_file) as f:
        data = f.read()
        return data[:100] + "..." if len(data) > 100 else data


@bp.route('/pastes/<filename>')
def paste_file(filename):
    """
    serve the file (triggered when user clicks "View" on a file)
    """
    return send_from_directory(current_app.config['PASTES_FOLDER'], filename)


@bp.route('/delete/<shortlink>')
def delete_paste(shortlink):
    """
    delete the paste and the file (triggered when user clicks "Delete" on a file)
    """
    paste = Paste.query.filter_by(shortlink=shortlink)
    if paste.one_or_none() is None:
        abort(400)
    elif paste.one_or_none().user_id != current_user.id:
        abort(403)
    paste.delete()
    db.session.commit()
    try:
        os.remove(f"{current_app.config['PASTES_FOLDER']}/{shortlink}.txt")
    except:
        pass
    flash('Deleted paste successfully!')
    return redirect(url_for('main.user', username=current_user.username))


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PasteForm(expires='Never')
    if form.tagbtn.data:  # add tag
        if form.tag.data and not Tag.query.filter_by(value=form.tag.data).first():
            if len(form.tag.data) > 16:
                form.tag.errors = ["tag is too long"]
            else:
                tag = Tag(value=form.tag.data)
                db.session.add(tag)
                db.session.commit()
        if form.tag.data and not form.tag.errors and form.tag.data not in PasteForm.paste_tags:
            PasteForm.paste_tags.append(form.tag.data)
    elif form.submit.data:  # submit
        if form.validate_on_submit():
            if current_user.pastes.count() >= current_app.config['USER_PASTES_LIMIT']:
                flash("You cannot create any more pastes!")
                return render_template('main/index.html', title='Home',
                                       form=form, paste_tags=PasteForm.paste_tags,
                                       paste_tags_ac_entries=[])
            # parse form info
            shortlink = generate_shortlink(
                request.remote_addr, str(datetime.utcnow()), 8)
            created_at = datetime.utcnow()
            expires_at = created_at + timedelta(hours=1) if form.expires.data == '1 Hour' else \
                created_at + timedelta(days=1) if form.expires.data == '1 Day' else \
                created_at + timedelta(weeks=1) if form.expires.data == '1 Week' else \
                sqlalchemy.null()
            paste_path = f"{current_app.config['PASTES_FOLDER']}/{shortlink}.txt"
            user_id = current_user.id
            json_metadata = json.dumps({"tags": PasteForm.paste_tags})
            # write data to file
            with open(paste_path, 'w') as f:
                f.write(form.paste.data)
            # add paste to database
            paste = Paste(shortlink=shortlink, created_at=created_at, expires_at=expires_at,
                          paste_path=paste_path, user_id=user_id, json_metadata=json_metadata)
            db.session.add(paste)
            db.session.commit()
            # reset static variables
            PasteForm.paste_tags = []
            flash("Your paste is now live!")
            return redirect(url_for('main.index'))
    # autocomplete entries
    paste_tags_ac_entries = [entry.value for entry in Tag.query.all()]
    return render_template('main/index.html', current_app=current_app,
                           form=form, paste_tags=PasteForm.paste_tags,
                           paste_tags_ac_entries=paste_tags_ac_entries)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    pastes = Paste.query.order_by(Paste.created_at.desc()).paginate(
        page, current_app.config['PASTES_PER_PAGE'], False)
    next_url = url_for('main.explore', page=pastes.next_num) \
        if pastes.has_next else None
    prev_url = url_for('main.explore', page=pastes.prev_num) \
        if pastes.has_prev else None
    return render_template('main/explore.html', pastes=pastes.items,
                           next_url=next_url, prev_url=prev_url, current_app=current_app,
                           get_preview=get_preview, parse_tags=parse_tags, read_only=True)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pastes = user.pastes.order_by(Paste.created_at.desc()).paginate(
        page, current_app.config['PASTES_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=pastes.next_num) \
        if pastes.has_next else None
    prev_url = url_for('main.user', username=user.username, page=pastes.prev_num) \
        if pastes.has_prev else None
    return render_template('main/user.html', user=user, pastes=pastes.items,
                           next_url=next_url, prev_url=prev_url, current_app=current_app,
                           get_preview=get_preview, parse_tags=parse_tags)
