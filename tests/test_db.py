from dataclasses import asdict

from sqlalchemy import select

from fastapi_webdev.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user = User(
            username='iurikill69',
            email='yurictorquato@gmail.com',
            password='123',
        )

        session.add(user)
        session.commit()

        result = session.scalar(
            select(User).where(User.username == 'iurikill69')
        )

    assert asdict(result) == {
        'id': 1,
        'username': 'iurikill69',
        'email': 'yurictorquato@gmail.com',
        'password': '123',
        'created_at': time,
        'updated_at': None,
    }
