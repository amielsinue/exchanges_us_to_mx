import json

from app.users.model import User
from .configtest import *


class TestRegister(BaseTest):

    def test_missing_required_args(self, client, session):
        response = client.post('/auth/register', data=json.dumps({"email": 'test@email.com'}))

        assert response.status_code == 400

    def test_new_user(self, client, session):
        response = client.post('/auth/register', data=json.dumps({"email": 'test@email.com', "password": "12345"}))

        assert response.status_code == 200

        data = response.json
        assert data.get('id') is not None
        assert data.get('email') == 'test@email.com'
        assert data.get('api_token') is not None

    def test_same_email_is_not_allowed(self, client, session):
        user = User(email='fulanito@email.com', password='12345')
        session.add(user)
        session.commit()

        response = client.post('/auth/register', data=json.dumps({"email": user.email, "password": "12345"}))

        assert response.status_code == 409
