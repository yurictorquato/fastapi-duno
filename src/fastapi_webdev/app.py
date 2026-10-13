from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()
database = []


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
def create_user(user: UserSchema) -> UserPublic:
    user_with_id = UserDB(
        id=len(database) + 1,
        username=user.username,
        email=user.email,
        password=user.password,
    )

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserList, status_code=HTTPStatus.OK)
def read_users():
    return {'users': database}


@app.get(
    path='/users/{id}',
    response_model=UserPublic,
    status_code=HTTPStatus.OK,
)
def read_user(id: int) -> UserPublic:
    if id > len(database) or id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    return database[id - 1]


@app.put('/users/{id}', response_model=UserPublic, status_code=HTTPStatus.OK)
def update_user(id: int, user: UserSchema) -> UserPublic:
    user_with_id = UserDB(**user.model_dump(), id=id)
    if id > len(database) or id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    database[id - 1] = user_with_id

    return user_with_id


@app.delete(
    path='/users/{id}',
    response_model=UserPublic,
    status_code=HTTPStatus.OK,
)
def delete_user(id: int) -> None:
    if id > len(database) or id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    return database.pop(id - 1)
