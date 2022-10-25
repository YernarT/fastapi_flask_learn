from fastapi import FastAPI, Body

from sqlalchemy.exc import NoResultFound, IntegrityError
from .db import User
from .utils import doSQL, getDBSession, is_authenticated

app = FastAPI()


@app.get('/users')
async def users():
    users = doSQL(
        lambda session: session.query(User).all()
    )

    return {'isSuccess': True, 'message': '', 'data': {
        'users': users
    }}


@app.get('/users/{id}')
async def users(id: int):
    response_context = {'message': ''}

    try:
        user = doSQL(
            lambda session: session.query(User).filter_by(id=id).one()
        )
        response_context['isSuccess'] = True
    except NoResultFound:
        user = None
        response_context['isSuccess'] = False
        response_context['message'] = 'User Not Found'

    response_context['data'] = {
        'user': user
    }

    return response_context


@app.post('/users')
async def users(fullname=Body(None), password=Body(None)):
    if fullname == None:
        return {'isSuccess': False, 'message': 'Fullname is required', 'data': None}
    if password == None:
        return {'isSuccess': False, 'message': 'Password is required', 'data': None}

    user = User(fullname=fullname, password=password)

    session = getDBSession()()
    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        return {'isSuccess': False, 'message': 'Fullname is already taken', 'data': None}

    return {'isSuccess': True, 'message': '', 'data': {
        'user': user
    }}


@app.put('/users/{id}')
async def users(id: int, uid=Body(None), fullname=Body(None), password=Body(None)):
    if uid == None:
        return {'isSuccess': False, 'message': 'Need Login First', 'data': None}
    else:
        if uid != id:
            return {'isSuccess': False, 'message': 'Can only modify own data', 'data': None}

        is_login = is_authenticated(uid)
        if not is_login:
            return {'isSuccess': False, 'message': 'Need Login First', 'data': None}

    if fullname == None:
        return {'isSuccess': False, 'message': 'Fullname is required', 'data': None}
    if password == None:
        return {'isSuccess': False, 'message': 'Password is required', 'data': None}

    session = getDBSession()()
    user = session.query(User).filter_by(id=uid).one()
    try:
        user.fullname = fullname
        user.password = password

        session.commit()
    except IntegrityError:
        return {'isSuccess': False, 'message': 'Fullname is already taken', 'data': None}

    return {'isSuccess': True, 'message': '', 'data': {
        'user': user
    }}


@app.delete('/users/{id}')
async def users(id: int, uid=Body(None)):
    if uid == None:
        return {'isSuccess': False, 'message': 'Need Login First', 'data': None}
    else:
        uid = uid['uid']
        if uid != id:
            return {'isSuccess': False, 'message': 'Can only delete own data', 'data': None}

        is_login = is_authenticated(uid)
        if not is_login:
            return {'isSuccess': False, 'message': 'Need Login First', 'data': None}

    session = getDBSession()()
    session.query(User).filter_by(id=uid).delete()
    session.commit()

    return {'isSuccess': True, 'message': 'Successfully deleted', 'data': None}


@app.post('/login')
async def login(fullname=Body(None), password=Body(None)):
    if fullname == None:
        return {'isSuccess': False, 'message': 'Fullname is required', 'data': None}
    if password == None:
        return {'isSuccess': False, 'message': 'Password is required', 'data': None}

    session = getDBSession()()
    try:
        user = session.query(User).filter_by(fullname=fullname).one()
    except NoResultFound:
        return {'isSuccess': False, 'message': 'Wrong fullname or password', 'data': None}

    if user.password != password:
        return {'isSuccess': False, 'message': 'Wrong fullname or password', 'data': None}

    user.is_login = True
    session.commit()

    return {'isSuccess': True, 'message': 'Login successful',
            'data': {'uid': user.id}}
