from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import get_session
from .models import User
from .schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá, mundo!'}


@app.get('/ola-mundo', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def exercicio():
    return """
    <html>
        <head>
            <title>Exercício</title>
        </head>
        <body>
            <h1>Olá, mundo do exercício!</h1>
        </body>
    </html>"""


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(
    user: UserSchema, session: Session = Depends(get_session)
) -> UserPublic:
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='E-mail already exists'
            )

    db_user = User(**user.model_dump())

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList, status_code=HTTPStatus.OK)
def read_users(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


@app.get(
    path='/users/{id}',
    response_model=UserPublic,
    status_code=HTTPStatus.OK,
)
def read_user(id: int, session: Session = Depends(get_session)) -> UserPublic:
    user_db = session.scalar(select(User).where(User.id == id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    return UserPublic.model_validate(user_db)


@app.put('/users/{id}', response_model=UserPublic, status_code=HTTPStatus.OK)
def update_user(
    id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
) -> UserPublic:
    user_db = session.scalar(select(User).where(User.id == id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    user_db = User(**user.model_dump())

    try:
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or E-mail already exists',
        )

    return user_db


@app.delete(
    path='/users/{id}',
    response_model=Message,
    status_code=HTTPStatus.OK,
)
def delete_user(id: int, session: Session = Depends(get_session)) -> Message:
    user_db = session.scalar(select(User).where(User.id == id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    session.delete(user_db)
    session.commit()

    return Message(message='User deleted')
