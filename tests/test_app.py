from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_webdev.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A: Act     - Executa a coisa (SUT - System Under Test)
    - A: Assert  - Garanta que A é A
    Essa é a taxonomia de um teste
    """
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, mundo!'}
