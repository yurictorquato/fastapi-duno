from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A: Act     - Executa a coisa (SUT - System Under Test)
    - A: Assert  - Garanta que A é A
    Essa é a taxonomia de um teste
    """

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, mundo!'}


def test_deve_retornar_ola_mundo_em_html(client):
    response = client.get('/ola-mundo')

    assert response.status_code == HTTPStatus.OK
    assert response.headers['content-type'] == 'text/html; charset=utf-8'

    html = response.text
    assert '<h1>Olá, mundo do exercício!</h1>' in html


def test_create_user(client):
    payload = {
        'username': 'iurikill69',
        'email': 'iurikillzone@gmail.com',
        'password': '123456',
    }

    response = client.post('/users/', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['id'] == 1
    assert response.json()['username'] == 'iurikill69'
    assert response.json()['email'] == 'iurikillzone@gmail.com'
    assert 'password' not in response.json()


def test_read_users(client):
    response = client.get('/users/')

    payload = {
        'users': [
            {
                'id': 1,
                'username': 'iurikill69',
                'email': 'iurikillzone@gmail.com',
            },
        ]
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == payload


def test_read_user(client):
    payload = {
        'id': 1,
        'username': 'iurikill69',
        'email': 'iurikillzone@gmail.com',
    }

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == payload


def test_read_user_not_found(client):
    response = client.get('/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client):
    payload = {
        'username': 'iurikillzone',
        'email': 'yurictorquato@gmail.com',
        'password': '123',
    }

    response = client.put('/users/1', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == 1
    assert response.json()['username'] == 'iurikillzone'
    assert response.json()['email'] == 'yurictorquato@gmail.com'


def test_update_user_not_found(client):
    payload = {
        'username': 'iurikillzone',
        'email': 'yurictorquato@gmail.com',
        'password': '123',
    }

    response = client.put('/users/-1', json=payload)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == 1
    assert response.json()['username'] == 'iurikillzone'
    assert response.json()['email'] == 'yurictorquato@gmail.com'


def test_delete_user_not_found(client):
    response = client.delete('/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND
