from tools import login, logout


def test_permissions(testclient):
    # create-permission
    logout(testclient)
    rv = testclient.post('/+upload', data={'text': 'test'})
    assert rv.status_code == 403
    login(testclient, 'c')
    rv = testclient.post('/+upload', data={'text': 'test'})
    assert rv.status_code == 302  # expect redirect (to /+read)
    paste_id = rv.headers['Location'].split('/')[-1].replace('#None', '')

    # read-permission
    logout(testclient)
    rv = testclient.get('/' + paste_id)
    assert rv.status_code == 403
    login(testclient, 'r')
    rv = testclient.get('/' + paste_id)
    assert rv.status_code == 200

    # admin-permission
    logout(testclient)
    # lock
    rv = testclient.post('/{}/+lock'.format(paste_id))
    assert rv.status_code == 403
    login(testclient, 'a')
    rv = testclient.post('/{}/+lock'.format(paste_id))
    assert rv.status_code == 302
    rv = testclient.post('/{}/+unlock'.format(paste_id))
    assert rv.status_code == 302

    # delete-permission
    logout(testclient)
    rv = testclient.post('/{}/+delete'.format(paste_id))
    assert rv.status_code == 403
    login(testclient, 'd')
    rv = testclient.post('/{}/+delete'.format(paste_id))
    assert rv.status_code == 302

    # list-permission
    logout(testclient)
    rv = testclient.get('/+list')
    assert rv.status_code == 403
    login(testclient, 'l')
    rv = testclient.get('/+list')
    assert rv.status_code == 200
