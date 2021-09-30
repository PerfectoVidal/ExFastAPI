from users.models import User


class TestUSer:
    def test_repr(self):
        u = User(name='foo', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='foo@gmail.com', is_superuser=False)
        assert u.__repr__() == 'foo surfoo1 surfoo2'

    def test_str(self):
        u = User(name='foo', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='foo@gmail.com', is_superuser=False)
        assert str(u) == 'foo surfoo1 surfoo2'
