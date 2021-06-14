import json

from app.users.model import User
from .configtest import *


class TestLogin(BaseTest):

    def test_invalid_credentials(self, client, session):
        response = client.post('/auth/login', data=json.dumps({"email": 'none@email.com', "password": "12345"}))

        assert response.status_code == 404

        user = User(email='none@gmail.com', password='123456789')
        session.add(user)
        session.commit()

        response = client.post('/auth/login', data=json.dumps({"email": 'none@email.com', "password": "12345"}))

        assert response.status_code == 404

    def test_success(self, client, session):
        user = User(email='success@gmail.com', password='123456789')
        session.add(user)
        session.commit()

        response = client.post('/auth/login', data=json.dumps({"email": 'success@gmail.com', "password": "123456789"}))

        assert response.status_code == 200

        data = response.json
        assert data.get('id') is not None
        assert data.get('email') == 'success@gmail.com'
        assert data.get('api_token') is not None