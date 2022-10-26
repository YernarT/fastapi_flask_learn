from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.exc import NoResultFound, IntegrityError
from .db import User
from .utils import doSQL, getDBSession, is_authenticated

app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/users')
async def users():
    users = doSQL(
        lambda session: session.query(User).all()
    )

    return {'is_success': True, 'message': '', 'data': {
        'users': users
    }}


@app.get('/users/{id}')
async def users(id: int):
    response_context = {'message': ''}

    try:
        user = doSQL(
            lambda session: session.query(User).filter_by(id=id).one()
        )
        response_context['is_success'] = True
    except NoResultFound:
        user = None
        response_context['is_success'] = False
        response_context['message'] = 'User Not Found'

    response_context['data'] = {
        'user': user
    }

    return response_context


@app.post('/users')
async def users(fullname=Body(None), password=Body(None)):
    if fullname == None:
        return {'is_success': False, 'message': 'Fullname is required', 'data': None}
    if password == None:
        return {'is_success': False, 'message': 'Password is required', 'data': None}

    user = User(fullname=fullname, password=password)

    session = getDBSession()()
    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        return {'is_success': False, 'message': 'Fullname is already taken', 'data': None}

    return {'is_success': True, 'message': 'Registration success', 'data': {
        'user': user
    }}


@app.put('/users/{id}')
async def users(id: int, uid=Body(None), fullname=Body(None), password=Body(None)):
    if uid == None:
        return {'is_success': False, 'message': 'Need Login First', 'data': None}
    else:
        if uid != id:
            return {'is_success': False, 'message': 'Can only modify own data', 'data': None}

        is_login = is_authenticated(uid)
        if not is_login:
            return {'is_success': False, 'message': 'Need Login First', 'data': None}

    if fullname == None:
        return {'is_success': False, 'message': 'Fullname is required', 'data': None}
    if password == None:
        return {'is_success': False, 'message': 'Password is required', 'data': None}

    session = getDBSession()()
    user = session.query(User).filter_by(id=uid).one()
    try:
        user.fullname = fullname
        user.password = password

        session.commit()
    except IntegrityError:
        return {'is_success': False, 'message': 'Fullname is already taken', 'data': None}

    return {'is_success': True, 'message': '', 'data': {
        'user': user
    }}


@app.delete('/users/{id}')
async def users(id: int, uid=Body(None)):
    if uid == None:
        return {'is_success': False, 'message': 'Need Login First', 'data': None}
    else:
        uid = uid['uid']
        if uid != id:
            return {'is_success': False, 'message': 'Can only delete own data', 'data': None}

        is_login = is_authenticated(uid)
        if not is_login:
            return {'is_success': False, 'message': 'Need Login First', 'data': None}

    session = getDBSession()()
    session.query(User).filter_by(id=uid).delete()
    session.commit()

    return {'is_success': True, 'message': 'Successfully deleted', 'data': None}


@app.get('/is_logged/{uid}')
async def is_logged(uid: int):
    session = getDBSession()()
    try:
        user = session.query(User).filter_by(id=uid).one()
    except NoResultFound:
        return {'is_success': False, 'message': 'Non-existent user', 'data': None}

    return {'is_success': True, 'message': '',
            'data': {'is_login': user.is_login}}


@app.post('/login')
async def login(fullname=Body(None), password=Body(None)):
    if fullname == None:
        return {'is_success': False, 'message': 'Fullname is required', 'data': None}
    if password == None:
        return {'is_success': False, 'message': 'Password is required', 'data': None}

    session = getDBSession()()
    try:
        user = session.query(User).filter_by(fullname=fullname).one()
    except NoResultFound:
        return {'is_success': False, 'message': 'Wrong fullname or password', 'data': None}

    if user.password != password:
        return {'is_success': False, 'message': 'Wrong fullname or password', 'data': None}

    user.is_login = True
    session.commit()

    return {'is_success': True, 'message': 'Login successful',
            'data': {'uid': user.id}}


@app.post('/logout/{uid}')
async def logout(uid: int):
    session = getDBSession()()
    try:
        user = session.query(User).filter_by(id=uid).one()
    except NoResultFound:
        return {'is_success': False, 'message': 'Non-existent user', 'data': None}

    user.is_login = False
    session.commit()

    return {'is_success': True, 'message': 'Logout smoothly', 'data': None}
