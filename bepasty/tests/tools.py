def login(testclient, token):
    return testclient.post(
        '/+login', data={'token': token},
        follow_redirects=True
    )


def logout(testclient):
    return testclient.post('/+logout', follow_redirects=True)
