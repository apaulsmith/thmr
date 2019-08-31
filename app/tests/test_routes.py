from app.tests import data_generator


def test_login(flask_client):
    logout(flask_client)

    response = login(flask_client, 'bad_email', 'bad_password')
    assert 'Please Sign In' in str(response.data)

    response = login(flask_client, data_generator.TEST_ACCOUNT_EMAIL, data_generator.TEST_ACCOUNT_PASSWORD)
    assert 'Please Sign In' not in str(response.data)


def test_patient_search(flask_client):
    login(flask_client, data_generator.TEST_ACCOUNT_EMAIL, data_generator.TEST_ACCOUNT_PASSWORD)
    response = flask_client.post('/patient_search', data=dict(name='smith', gender=''), follow_redirects=True)
    assert response.status == '200 OK'
    assert 'Smith,' in str(response.data)


def login(flask_client, username, password):
    return flask_client.post('/login', data=dict(
        username=username,
        password=password,
    ), follow_redirects=True)


def logout(flask_client):
    return flask_client.get('/logout', follow_redirects=True)
