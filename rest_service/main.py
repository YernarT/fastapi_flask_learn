from fastapi import FastAPI, Body

from sqlalchemy.exc import NoResultFound, IntegrityError
from .db import doSQL, getDBSession, User

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
    try:
        user = doSQL(
            lambda session: session.query(User).filter_by(id=id).one()
        )
    except NoResultFound:
        user = {'message': 'User Not Found'}

    return {'isSuccess': True, 'message': '', 'data': {
        'user': user
    }}


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
    
    print(user)

    return {'isSuccess': True, 'message': '', 'data': {
        'user': {}
    }}


@app.put('/users')
async def users():
    return {'isSuccess': True, 'message': '', 'data': {
        'user': {}
    }}


@app.patch('/users')
async def users():
    return {'isSuccess': True, 'message': '', 'data': {
        'user': {}
    }}


@app.delete('/users')
async def users():
    return {'isSuccess': True, 'message': '', 'data': None}
