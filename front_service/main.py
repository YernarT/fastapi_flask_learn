from flask import Flask, render_template, request, redirect, url_for

from utils.auth import get_user
from utils.serializer import obj_to_json

app = Flask(__name__)


@app.route('/')
def index():
    user = get_user(request)

    context = {
        'user': user,
        'serialized_user': obj_to_json(user)
    }

    return render_template('index.html', context=context)


@app.route('/login')
def login():
    user = get_user(request)

    context = {
        'user': user,
        'serialized_user': obj_to_json(user)
    }

    return render_template('login.html', context=context)


@app.route('/register')
def register():
    user = get_user(request)

    context = {
        'user': user,
        'serialized_user': obj_to_json(user)
    }

    return render_template('register.html', context=context)


@app.route('/logout')
def logout():
    user = get_user(request)
    uid = user['id']

    import requests

    requests.post(
        f'http://127.0.0.1:8000/logout/{uid}').json()

    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    user = get_user(request)
    uid = user['id']

    if not user['is_login']:
        return render_template('page_not_found.html')

    import requests

    response = requests.get(
        f'http://127.0.0.1:8000/resume/{uid}').json()

    if not response['data']:
        return redirect(url_for('create_resume'))

    context = {
        'user': user,
        'serialized_user': obj_to_json(user),

        'data': response['data'],
        'serialized_resume': obj_to_json(response['data']),
    }

    return render_template('profile.html', context=context)


@app.route('/create_resume')
def create_resume():
    user = get_user(request)
    uid = user['id']

    if not user['is_login']:
        return render_template('page_not_found.html')

    return render_template('create_resume.html')


@app.route('/404')
def page_not_found():

    return render_template('page_not_found.html')


if __name__ == '__main__':
    app.debug = True
    # app.secret_key = 'N0GiuzUGHkrbfGRazAV2QgxAZy3AJWHd'
    app.run()
