from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Query

from main import app
from tests.utils import the_list_contain_the_same_elements
from src.users.models import User

client = TestClient(app)


class TestRouters:

    def test_read_all_users_empty(self, dbsession):
        with patch('src.users.routers.session', new=dbsession):
            response = client.get("/users/")
            assert all([response.status_code == 200,
                        response.json() is None])

    def test_read_all_users(self, dbsession):
        with patch('src.users.routers.session', new=dbsession):
            users = [User(name='foo', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='foo@gmail.com', is_superuser=False),
                     User(name='foo2', surname_1='surfoo12', surname_2='surfoo22', password='1234', email='foo2@gmail.com', is_superuser=False), ]
            result = [{'email': 'foo@gmail.com', 'name': 'foo', 'surname_1': 'surfoo1', 'surname_2': 'surfoo2'},
                      {'email': 'foo2@gmail.com', 'name': 'foo2', 'surname_1': 'surfoo12', 'surname_2': 'surfoo22'}]
            dbsession.bulk_save_objects(users)
            dbsession.commit()
            response = client.get("/users/")
            assert all([response.status_code == 200,
                        the_list_contain_the_same_elements(response.json()['results'], result)])

    def test_create_user_error(self):
        response = client.post("/users/", data={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user(self, dbsession):
        info = [{'name': 'foo', 'surname_1': 'surfoo1', 'surname_2': 'surfoo2', 'password': '1234', 'email': 'foo@gmail.com'},
                {'name': 'foo2', 'surname_1': 'surfoo12', 'surname_2': 'surfoo22', 'password': '1234', 'email': 'foo2@gmail.com'}]
        with patch('src.users.routers.session', new=dbsession):
            for data in info:
                response = client.post("/users/", json=data)
        q = Query([User], session=dbsession).all()
        assert all([response.status_code == status.HTTP_201_CREATED,
                    len(q) == 2,
                    q[0].is_superuser is False,
                    the_list_contain_the_same_elements(['foo', 'foo2'], [el.name for el in q])])

    def test_search_user_empty(self, dbsession):
        with patch('src.users.routers.session', new=dbsession):
            response = client.get("/users/foo")
            assert all([response.status_code == status.HTTP_404_NOT_FOUND,
                        response.json() == {'detail': 'The user with name foo not found'}])

    def test_post_and_search(self, dbsession):
        info = [{'name': 'foo', 'surname_1': 'surfoo1', 'surname_2': 'surfoo2', 'password': '1234', 'email': 'foo@gmail.com'},
                {'name': 'foo2', 'surname_1': 'surfoo12', 'surname_2': 'surfoo22', 'password': '1234', 'email': 'foo2@gmail.com'}]
        with patch('src.users.routers.session', new=dbsession):
            for data in info:
                client.post("/users/", json=data)
            response = client.get("/users/foo")
        assert all([response.status_code == 200,
                    response.json() == {'name': 'foo', 'surname_1': 'surfoo1', 'surname_2': 'surfoo2', 'email': 'foo@gmail.com'}])
