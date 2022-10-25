from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    fullname = Column('fullname', String(40), unique=True)
    password = Column('password', String(254))
    is_login = Column('is login', Boolean())

    resumes = relationship('Resume', back_populates='user')

    def __str__(self):
        return f'{self.fullname}'


class Resume(Base):
    __tablename__ = 'resume'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='resumes')

    position = Column('position', String(40))
    country = Column('country', String(20))
    address = Column('address', String(40))
    phone = Column('phone', String(24))
    email = Column('email', String(254))
    site = Column('site', String(128))
    about_me = Column('about_me', String(254))

    work_experiences = relationship('WorkExperience', back_populates='resume')
    educations = relationship('Education', back_populates='resume')
    skills = relationship('Skill', back_populates='resume')
    socials = relationship('Social', back_populates='resume')

    def __str__(self):
        return f'{self.email}'


class WorkExperience(Base):
    __tablename__ = 'work_experience'

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resume.id'))
    resume = relationship('Resume', back_populates='work_experiences')

    date_from = Column('date from', String(10))
    date_to = Column('date to', String(10))
    workspace = Column('workspace', String(40))
    description = Column('description', String(254))

    def __str__(self):
        return f'{self.workspace}'


class Education(Base):
    __tablename__ = 'education'

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resume.id'))
    resume = relationship('Resume', back_populates='educations')

    date_from = Column('date from', String(10))
    date_to = Column('date to', String(10))
    agency = Column('agency', String(40))
    description = Column('description', String(254))

    def __str__(self):
        return f'{self.agency}'


class Skill(Base):
    __tablename__ = 'skill'

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resume.id'))
    resume = relationship('Resume', back_populates='skills')

    name = Column('name', String(20))
    level = Column('level', Integer)

    def __str__(self):
        return f'{self.name}'


class Social(Base):
    __tablename__ = 'social'

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resume.id'))
    resume = relationship('Resume', back_populates='socials')

    name = Column('name', String(20))
    url = Column('url', String(128))

    def __str__(self):
        return f'{self.name}'
