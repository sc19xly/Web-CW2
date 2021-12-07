from werkzeug.security import generate_password_hash

from test import helpers

from website import db
from website.models import User, Post, Comment


class TestReply:
    def test_get_comment(self, test_client):
        """
        Test GET request to the /comment route to assert the create
        comment page is displayed.
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
            f"/create-comment/{post.id}"
        )

        assert response is not None
        assert response.status_code == 302

    def test_post_reply(self, test_client):
        """
        Test POST request to the /community/_/post/_/reply route to assert the reply is
        successfully created.
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
            f"/create-comment/{post.id}",
            data={"text": "username"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"username" in response.data


    def test_post_delete_reply(self, test_client):
        """
        Test POST request to the /community/_/post/_/reply/_/delete route to assert the
        reply is successfully deleted.
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
        comment = Comment(text="username", author=app_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()

        helpers.login(test_client, email, password)

        response = test_client.get(
            f"/delete-comment/{comment.id}"
        )

        assert response is not None
        assert response.status_code == 302
        assert b"username" not in response.data

