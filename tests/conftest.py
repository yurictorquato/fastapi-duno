from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

from fastapi_webdev.app import app
from fastapi_webdev.database import get_session
from fastapi_webdev.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2026, 10, 14)):
    def fake_time_hook(_mapper, _connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

    def fake_update_hook(_mapper, _connection, target):
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    event.listen(model, 'before_update', fake_update_hook)

    try:
        yield time
    finally:
        event.remove(model, 'before_insert', fake_time_hook)
        event.remove(model, 'before_update', fake_update_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: Session):
    user = User(
        username='yuri', email='yurictorquato@gmail.com', password='123'
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
