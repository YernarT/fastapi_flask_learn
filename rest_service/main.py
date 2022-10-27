from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.exc import NoResultFound, IntegrityError
from .db import User, Resume, WorkExperience, Education, Skill
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


@app.get('/resume/{uid}')
async def resume(uid: int):
    if uid == None:
        return {'is_success': False, 'message': 'Need Login First', 'data': None}
    else:
        is_login = is_authenticated(uid)
        if not is_login:
            return {'is_success': False, 'message': 'Need Login First', 'data': None}

    session = getDBSession()()
    try:
        user = session.query(User).filter_by(id=uid).one()
    except NoResultFound:
        return {'is_success': False, 'message': 'Non-existent user', 'data': None}

    result = {}
    if not user.resumes:
        result = None
    else:
        resume = user.resumes[0]

        result['resume'] = resume
        result['work_experiences'] = resume.work_experiences
        result['educations'] = resume.educations
        result['skills'] = resume.skills

    return {'is_success': True, 'message': '', 'data': result}


@app.post('/resume/{uid}')
async def resume(uid: int,
                 position=Body(None),
                 country=Body(None),
                 address=Body(None),
                 phone=Body(None),
                 email=Body(None),
                 site=Body(None),
                 about_me=Body(None),
                 facebook=Body(None),
                 twitter=Body(None),
                 youtube=Body(None),
                 linkedin=Body(None)):
    if uid == None:
        return {'is_success': False, 'message': 'Need Login First', 'data': None}
    else:
        is_login = is_authenticated(uid)
        if not is_login:
            pass
            # return {'is_success': False, 'message': 'Need Login First', 'data': None}

    session = getDBSession()()
    try:
        user = session.query(User).filter_by(id=uid).one()
    except NoResultFound:
        return {'is_success': False, 'message': 'Non-existent user', 'data': None}

    if user.resumes:
        pass
        # return {'is_success': False, 'message': 'Already have resume', 'data': None}
    else:

        resume = Resume(user_id=uid,
                        position=position,
                        country=country,
                        address=address,
                        phone=phone,
                        email=email,
                        site=site,
                        about_me=about_me,
                        facebook=facebook,
                        twitter=twitter,
                        youtube=youtube,
                        linkedin=linkedin)

        session = getDBSession()()
        session.add(resume)
        session.commit()

        work_experience1 = WorkExperience(
                resume_id=1,
                date_from=2022,
                date_to=None,
                workspace='IT IS IT',
                description='''
                Lorem, ipsum dolor sit amet consectetur adipisicing elit. Porro ratione labore assumenda nostrum voluptate unde minima voluptatibus accusamus! Consequatur provident, cum vero ducimus accusantium nam nisi commodi tempora alias laborum.
                ''',
            )
        work_experience2 = WorkExperience(
                resume_id=1,
                date_from=2020,
                date_to=2022,
                workspace='Google',
                description='''
                Lorem, ipsum dolor sit amet consectetur adipisicing elit. Porro ratione labore assumenda nostrum voluptate unde minima voluptatibus accusamus! Consequatur provident, cum vero ducimus accusantium nam nisi commodi tempora alias laborum.
                ''',
            )
        work_experience3 = WorkExperience(
                resume_id=1,
                date_from=2016,
                date_to=2020,
                workspace='Halyk Bank',
                description='''
                Lorem, ipsum dolor sit amet consectetur adipisicing elit. Porro ratione labore assumenda nostrum voluptate unde minima voluptatibus accusamus! Consequatur provident, cum vero ducimus accusantium nam nisi commodi tempora alias laborum.
                ''',
        )

        education1 = Education(
                resume_id=1,
                date_from=2016,
                date_to=2012,
                agency='Astana IT Univercity',
                description='''
                Lorem, ipsum dolor sit amet consectetur adipisicing elit. Porro ratione labore assumenda nostrum voluptate unde minima voluptatibus accusamus! Consequatur provident, cum vero ducimus accusantium nam nisi commodi tempora alias laborum.
                ''',
            )
        education2 = Education(
                resume_id=1,
                date_from=2001,
                date_to=2012,
                agency='Astana No.73 High Scholl',
                description='''
                Lorem, ipsum dolor sit amet consectetur adipisicing elit. Porro ratione labore assumenda nostrum voluptate unde minima voluptatibus accusamus! Consequatur provident, cum vero ducimus accusantium nam nisi commodi tempora alias laborum.
                ''',
        )

        skill1 = Skill(resume_id=1, name='HTML5', level=85)
        skill2 = Skill(resume_id=1, name='CSS3', level=75)
        skill3 = Skill(resume_id=1, name='JavaScript', level=94)
        skill4 = Skill(resume_id=1, name='Python', level=88)
        

        # for work_experience in work_experiences:
        session = getDBSession()()
        session.add(work_experience1)
        session.add(work_experience2)
        session.add(work_experience3)
        session.commit()
        # for education in educations:
        session = getDBSession()()
        session.add(education1)
        session.add(education2)
        session.commit()
        # for skill in skills:
        session = getDBSession()()
        session.add(skill1)
        session.add(skill2)
        session.add(skill3)
        session.add(skill4)
        session.commit()

    return {'is_success': True, 'message': 'Create resume successfully', 'data': None}
