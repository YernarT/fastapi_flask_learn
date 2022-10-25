from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def getDBSession():
    from .db import Base

    engine = create_engine('sqlite:///database.db')
    Base.metadata.create_all(engine)

    return sessionmaker(bind=engine)


# sql param only supports lambda functions
def doSQL(sql):
    session = getDBSession()()
    result = sql(session)

    return result


def is_authenticated(uid: int) -> bool:
    from sqlalchemy.exc import NoResultFound
    from .db import User

    try:
        user = doSQL(lambda session: session.query(User).filter_by(id=uid).one())
    except NoResultFound:
        return False
    
    return user.is_login