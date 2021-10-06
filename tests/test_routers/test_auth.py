from unittest.mock import patch, Mock

import pytest
from fastapi import HTTPException
from pydantic import EmailStr

from src.models.users import User
from src.routers.v1.auth import login, get_me, user_loader
from src.schemas.users import UserResult


class TestAuth:
    def test_login_not_user(self, dbsession):
        with pytest.raises(HTTPException)as exception:
            with patch('src.routers.v1.auth.db_session', return_value=dbsession):
                login(data=Mock(username='foo@gmail.com',
                                password='1234'))
        assert all([exception.value.status_code == 401,
                    exception.value.detail == 'Invalid credentials'])

    def test_login_invalid_password(self, dbsession):
        with pytest.raises(HTTPException)as exception:
            with patch('src.routers.v1.auth.db_session', return_value=dbsession):
                dbsession.add(User(name='foo', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='foo@gmail.com', is_superuser=False))
                dbsession.commit()
                login(data=Mock(username='foo@gmail.com',
                                password='12345'))
        assert all([exception.value.status_code == 401,
                    exception.value.detail == 'Invalid credentials'])

    def test_login(self, dbsession):
        with patch('src.routers.v1.auth.db_session', return_value=dbsession):
            dbsession.add(User(name='foo', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='foo@gmail.com', is_superuser=False))
            dbsession.commit()
            dict_acces_token = login(data=Mock(username='foo@gmail.com', password='1234'))
        assert all(['access_token' in dict_acces_token,
                    dict_acces_token['token_type'] == 'bearer'])

    def test_get_me(self):
        result = get_me(User(name='foo', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='foo@gmail.com', is_superuser=False).__dict__)
        assert result == {'user': UserResult(name='foo', surname_1='surfoo1', surname_2='surfoo2', email=EmailStr('foo@gmail.com'))}

    def test_user_loader(self, dbsession):
        with patch('src.routers.v1.auth.db_session', return_value=dbsession):
            dbsession.add(User(name='foo', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='foo@gmail.com', is_superuser=False))
            dbsession.commit()
            results = user_loader(email='foo@gmail.com')
            expected = {'surname_2': 'surfoo2',
                        'email': 'foo@gmail.com',
                        'is_superuser': False,
                        'name': 'foo',
                        'surname_1': 'surfoo1',
                        'password': '1234'}
            assert all([key in results and results[key] == expected[key] for key in expected])
