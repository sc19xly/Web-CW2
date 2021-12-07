from test import helpers
from werkzeug.security import generate_password_hash
from website import db
from website.models import User, Post, Like


class TestPost:
    def test_get_post(self, test_client):
        """
        Test GET request to the /home route to assert the community's
        post page is displayed.
        """
        password = "mockpassword"
        username = "mockusername"
        app_user = User(username=username, email="1204863763@qq.com", password=generate_password_hash(
            password, method='Sha256'))
        db.session.add(app_user)
        db.session.commit()
        helpers.post(test_client, app_user.email, password)
        response = test_client.get('/home')

        assert response is not None
        assert response.status_code == 200
        assert b'mockusername' in response.data

    def test_get_user_post(self, test_client):
        """
        Test GET request to the /community/_/post/_/top route to assert the community's
        post page is displayed.
        """
        password = "mockpassword"
        search_username = "username"
        username = "mockusername"
        app_user = User(username="mockusername", email="1204863763@qq.com", password=generate_password_hash(
            password, method='Sha256'))
        search_user = User(username="username", email="2773004372@qq.com", password=generate_password_hash(
            password, method='Sha256'))
        post1 = Post(text="mockusername", author=username)
        post2 = Post(text="mockusername", author=search_username)
        db.session.add(search_user)
        db.session.add(app_user)
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()
        helpers.login(test_client, app_user.email, password)

        response = test_client.get(
            f"/posts/{username}"
        )

        assert response is not None
        assert response.status_code == 200
        assert b'mockusername\'s posts'

    def test_post_create_post(self, test_client):
        """
        Test POST request to the /create-post route to assert the post is
        created successfully.
        """
        password = "Mockpassword123!"
        hashed_password = generate_password_hash(
            password, method='Sha256')
        app_user = User(username="mockusername", password=hashed_password)
        db.session.add(app_user)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.post(
            "/create-post",
            data={"text": "mockposttitle"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Back" not in response.data

        response = test_client.post(
            "/create-post",
            data={"text": None},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Create a Post" not in response.data

    def test_post_delete_post(self, test_client):
        """
        Test POST request to the /community/_/post/_/delete route to assert the post is
        deleted successfully.
        """
        password = "mockpassword"
        username = "mockusername"
        app_user = User(username=username, email="1204863763@qq.com", password=generate_password_hash(
            password, method='Sha256'))
        db.session.add(app_user)
        db.session.commit()
        helpers.post(test_client, app_user.email, password)

        response = test_client.get(
            "/delete-post/<post.id>",
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200

    def test_post_like_post(self, test_client):
        """
        Test POST request to the /like-post route to assert the user
        successfully upvotes the post.
        """
        password = "mockpassword"
        username = "mockusername"
        email = "1204863763@qq.com"
        app_user = User(username=username, email="1204863763@qq.com", password=generate_password_hash(
            password, method='Sha256'))
        post = Post(text="mockusername", author=username)
        db.session.add(app_user)
        db.session.add(post)
        db.session.commit()

        helpers.login(test_client, email, password)

        response = test_client.post(
            f"/like-post/{post.id}"
        )

        assert response is not None
        assert response.status_code == 200
        post_vote = Like.query.filter_by(
            author=app_user.id, post_id=post.id
        ).first()
        assert post_vote is not None
