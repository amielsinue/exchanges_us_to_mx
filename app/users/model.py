import binascii
import random
from datetime import datetime
from random import SystemRandom
from secrets import token_hex, token_bytes

from backports.pbkdf2 import pbkdf2_hmac, compare_digest
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property
from app.data import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _password = db.Column(db.LargeBinary(120))
    _salt = db.Column(db.LargeBinary(16))
    email = db.Column(db.String(120), unique=True, nullable=False)
    api_token = db.Column(db.String(120), nullable=True)
    api_token_created_at = db.Column(db.DateTime(), nullable=True)
    max_requests_count = db.Column(db.Integer, nullable=False, default=10)

    def __repr__(self):
        return '<User %r>' % self.username

    @hybrid_property
    def password(self):
        return self._password

    def is_valid_password(self, password):
        new_hash = self._hash_password(password, 30)
        if new_hash and self._password and compare_digest(new_hash, self._password):
            return True
        return False

    # In order to ensure that passwords are always stored
    # hashed and salted in our database we use a descriptor
    # here which will automatically hash our password
    # when we provide it (i. e. user.password = "12345")
    @password.setter
    def password(self, value):
        # When a user is first created, give them a salt
        if self._salt is None:
            res = bytes(random.randrange(0, 255) for _ in range(16))
            self._salt = res
        self._password = self._hash_password(value, 30)

    def _hash_password(self, password, iterations):
        try:
            pwd = password.encode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            # Already in unicode, no need to encode, Just continue
            pwd = password
        salt = bytes(self._salt, 'ascii') if type(self._salt) is not bytes else self._salt
        return bytes(pbkdf2_hmac("sha512", pwd, salt, iterations=iterations))

    def generate_api_token(self):
        self.api_token = token_hex(16)
        self.api_token_created_at = datetime.now()

    def on_create(cls, mapper, target):
        target.generate_api_token()


event.listen(User, 'before_insert', User.on_create)
