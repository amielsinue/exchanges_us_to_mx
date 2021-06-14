import mock
from datetime import datetime, timedelta

from app.users.model import User
from app.data import cache
from .configtest import *


class TestExchanges(BaseTest):

    def getUser(self, session, token_expired = False):
        user = User(email='{}@email.com'.format(random_char(7)), password='12345')
        session.add(user)
        session.commit()
        if token_expired:
            user.api_token_created_at = datetime.now() - timedelta(days=11)
            session.commit()
        return user

    def test_invalid_token(self, client, session):
        response = client.get('/exchanges')

        assert response.status_code == 401
        assert response.json.get('message') == 'Authentication required'

    def test_invalid_token(self, client, session):
        headers = auth_header('ASDFASDFEET')
        response = client.get(
            '/exchanges',
            headers=headers
        )

        assert response.status_code == 401
        assert response.json.get('message') == 'Invalid Token'

    def test_expired_token(self, client, session):
        user = self.getUser(session, True)
        headers = auth_header(user.api_token)
        response = client.get(
            '/exchanges',
            headers=headers
        )

        assert response.status_code == 401
        assert response.json.get('message') == 'Token Expired'

    @mock.patch('libs.banxico.parse_today')
    @mock.patch('libs.fixer.parse_today')
    @mock.patch('libs.diario.parse_today')
    def test_retrieving(self, banxico_mock, fixer_mock, diario_mock, client, session):
        banxico_mock.return_value = (datetime.now(), 19.9)
        fixer_mock.return_value = (datetime.now(), 19.9)
        diario_mock.return_value = (datetime.now(), 19.9)
        # TODO: remove this when we can figure out why mocks doesn't work
        cache.set('banxico_parse_today', (datetime.now(), 19.9))
        cache.set('diario_parse_today', (datetime.now(), 19.9))
        cache.set('fixer_parse_today', (datetime.now(), 19.9))

        user = self.getUser(session)
        headers = auth_header(user.api_token)
        response = client.get(
            '/exchanges?date={}'.format((datetime.now()-timedelta(days=-1)).strftime('%Y-%m-%d')),
            headers=headers
        )

        assert response.status_code == 200
        assert 'rates' in response.json
        rates = response.json.get('rates')
        assert 'banxico' in rates
        assert 'diario' in rates
        assert 'fixer' in rates

    def test_reach_limit(self, client, session):
        # TODO: remove this when we can figure out why mocks doesn't work
        cache.set('banxico_parse_today', (datetime.now(), 19.9))
        cache.set('diario_parse_today', (datetime.now(), 19.9))
        cache.set('fixer_parse_today', (datetime.now(), 19.9))

        user = self.getUser(session)
        user.max_requests_count = 1
        session.add(user)
        session.commit()
        headers = auth_header(user.api_token)
        response = client.get(
            '/exchanges?date={}'.format((datetime.now() - timedelta(days=-1)).strftime('%Y-%m-%d')),
            headers=headers
        )
        assert response.status_code == 401
        assert response.json.get('message') == 'Reached requests limit, please try again later'


