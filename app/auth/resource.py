from flask_restful import marshal_with
from app.libs.resource import BaseResource
from app.users.model import User
from app.users.serializer import user_auth

from app.data import db


class Auth(BaseResource):

    def _check_required_args(self):
        email = self.data.get('email')
        password = self.data.get('password')

        if email is None or password is None:
            self.abort(400)


class Login(Auth):

    @marshal_with(user_auth)
    def post(self):
        self._check_required_args()

        email = self.data.get('email')
        password = self.data.get('password')

        user = User.query.filter(User.email == email).first()
        if not user or not user.is_valid_password(password):
            # for security reasons do not specify if the password doesn't matches or users doesn't exists
            self.abort(404, message="Invalid credentials")

        user.generate_api_token()
        db.session.add(user)
        db.session.commit()

        return user


class Register(Auth):

    @marshal_with(user_auth)
    def post(self):
        self._check_required_args()

        email = self.data.get('email')
        password = self.data.get('password')

        if User.query.filter(User.email == email).first():
            self.abort(409, message="user already exists")

        user = User(email=email, password=password)

        db.session.add(user)
        db.session.commit()
        return user