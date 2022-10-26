from flask import Flask, render_template, request

from utils import auth, serializer

app = Flask(__name__)


@app.route('/')
def index():
    context = {
        'user': serializer.obj_to_json(auth.get_user(request))
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


if __name__ == '__main__':
    app.debug = True
    # app.secret_key = 'N0GiuzUGHkrbfGRazAV2QgxAZy3AJWHd'
    app.run()
