def login(test_client, email, password):
    """
    Helper to log in a user with the test client.
    """
    test_client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )


def post(test_client, email, password):
    """
        Helper to create a post with the test client.
        """
    login(test_client, email, password)
    test_client.post(
        "/create-post",
        data={"text": "mockusername"},
        follow_redirects=True,
    )
