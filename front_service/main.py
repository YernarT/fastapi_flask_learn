from flask import Flask, render_template, request, redirect, url_for

from utils.auth import get_user
from utils.serializer import obj_to_json

app = Flask(__name__)

fallback_user = {
    'is_login': False
}


@app.route('/')
def index():
    user = get_user(request)

    if not user:
        user = fallback_user

    context = {
        'user': user,
        'serialized_user': obj_to_json(user)
    }

    return render_template('index.html', context=context)


@app.route('/login')
def login():
    context = {
        'user': serializer.obj_to_json(auth.get_user(request))
    }

    return render_template('login.html', context=context)


@app.route('/register')
def register():
    context = {
        'user': serializer.obj_to_json(auth.get_user(request))
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
    context = {
        'user': serializer.obj_to_json(auth.get_user(request))
    }

    return render_template('profile.html', context=context)


if __name__ == '__main__':
    app.debug = True
    # app.secret_key = 'N0GiuzUGHkrbfGRazAV2QgxAZy3AJWHd'
    app.run()
