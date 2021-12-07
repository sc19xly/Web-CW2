from werkzeug.security import generate_password_hash

from test import helpers


from website import db
from website.models import User


class TestAuth:
    def test_get_register(self, test_client):
        """
        Tests GET request to the /register route to assert the registration page is
        returned.
        """
        response = test_client.get("/sign_up")

        assert response is not None
        assert response.status_code == 200
        assert b"Sign Up" in response.data

    def test_post_register(self, test_client):
        """
        Test POST request to the /register route to assert the user is successfully
        registered.
        """
        response = test_client.post(
            "/sign_up",
            data={
                "email":"1204863763@qq.com",
                "username": "mockusername",
                "password1": "Mockpassword123!",
                "password2": "Mockpassword123!",
            },
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Posts" in response.data

    def test_get_login(self, test_client):
        """
        Test GET request to the /login route to assert the login page is returned.
        """
        response = test_client.get("/login")

        assert response is not None
        assert response.status_code == 200
        assert b"Login" in response.data


    def test_post_login(self, test_client):
        """
        Test POST request to the /login route to assert the user is successfully logged
        in.
        """
        password = "Mockpassword123!"
        username = "mockusername"
        app_user = User(email="1204863763@qq.com", username=username, password=generate_password_hash(
            password, method='Sha256'))
        db.session.add(app_user)
        db.session.commit()

        response = test_client.post(
            "/login",
            data={"email": app_user.email, "password": password},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Hello,mockusername!" in response.data

    def test_post_logout(self, test_client):
        """
        Test POST request to the /logout route to assert the user is successfully
        logged out.
        """
        password = "Mockpassword123!"
        email = "1204863763@qq.com"
        app_user = User(username="mockusername", email=email, password=generate_password_hash(password,
                                                                                              method='Sha256'))
        db.session.add(app_user)
        db.session.commit()
        helpers.login(test_client, app_user.email, password)
        response1 = test_client.get(
            "/logout",
            follow_redirects=True,
        )

        assert response1 is not None
        assert response1.status_code == 200
        assert b'Home' in response1.data
