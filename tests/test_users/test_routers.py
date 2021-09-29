from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from utils import the_list_contain_the_same_elements
from users.models import User

client = TestClient(app)


def test_read_all_users_empty(dbsession):
    with patch('users.routers.session', new=dbsession):
        response = client.get("/users/")
        assert response.status_code == 200
        assert response.json() is None


def test_read_all_users(dbsession):
    with patch('users.routers.session', new=dbsession):
        users = [User(name='foo', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='foo@gmail.com', is_superuser=False),
                 User(name='foo2', surname_1='surfoo12', surname_2='surfoo22', password='1234', email='foo2@gmail.com', is_superuser=False), ]
        result = [{'email': 'foo@gmail.com', 'name': 'foo', 'surname_1': 'surfoo1', 'surname_2': 'surfoo2'},
                  {'email': 'foo2@gmail.com', 'name': 'foo2', 'surname_1': 'surfoo12', 'surname_2': 'surfoo22'}]
        dbsession.bulk_save_objects(users)
        dbsession.commit()
        response = client.get("/users/")
        assert response.status_code == 200
        assert the_list_contain_the_same_elements(response.json()['results'], result)
