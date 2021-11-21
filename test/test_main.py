import unittest
import urllib
from flask import url_for
from flask_login import current_user
from flask import request
from flask_testing import TestCase

from app import db, create_app
from app.auth.models import User

class BaseTestCase(TestCase):

    def create_app(self):
        self.baseURL = 'http://localhost:5000/'
        return create_app('test')

    def setUp(self):
        # self.client = self.app.test_client()
        db.create_all()
        db.session.add(User("SerhiyTest", "SerhiyTest@gmail.com", "password"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_real_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.baseURL)
        self.assertEqual(response.code, 200)

    def test_VerifyUserClient(self):
        user=User.query.first()
        self.assertEqual(user.username, "SerhiyTest")
        self.assertIn('@', user.email)

    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)

class FlaskTestCase(BaseTestCase):
    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/auth/logIn', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        response = self.client.get('/auth/account', follow_redirects=True)
        self.assertIn(b"Remember Me", response.data)


class UserViewsTests(BaseTestCase):

    def test_login_page_loads(self):
        response = self.client.get('/auth/logIn')
        self.assertIn(b"Remember Me", response.data)

    def test_correct_register_and_login(self):
        with self.client:
            register_data = {'username': 'SergoM', 'email': 'serhoTest@gmail.com', 'password1': '1233', 'password2': '1233'}
            response = self.client.post('/auth/register', data=register_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            log_data = {'email': "serhoTest@gmail.com", 'password1': '1233'}
            response = self.client.post('/auth/logIn', data=log_data, follow_redirects=True)
            self.assert_200(response)

    def test_incorrect_login(self):
        response = self.client.post(
            '/auth/logIn',
            data=dict(email="wrong.email@email.ma", password1="wrong"),
            follow_redirects=True
        )
        self.assertIn('Invalid login!', response.data)

if __name__ == '__main__':
    unittest.main()
