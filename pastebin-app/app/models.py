from flask import url_for
import os
import base64
from hashlib import md5
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    pastes = db.relationship('Paste', backref='author', lazy='dynamic')
    token = db.Column(db.String(140))
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size
        )

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'paste_count': self.pastes.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128)
            }
        }

        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Paste(db.Model):
    shortlink = db.Column(db.String(8), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime)
    paste_path = db.Column(db.String(255), nullable=False)  # upload path
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    json_metadata = db.Column(db.Text)  # json

    def __repr__(self):
        return '<Paste {}>'.format(self.body)


class Tag(db.Model):
    """
    used for auto-completion
    """
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(16), unique=True, nullable=False)
