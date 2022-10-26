from flask import Flask, render_template, request

import requests

app = Flask(__name__)


@app.route('/')
def index():
    user = {}
    uid = request.cookies.get('uid')

    if uid is None:
        user['is_login'] = False
    else:
        response = requests.get(
            f'http://127.0.0.1:8000/is_logged/{uid}').json()
        if not response.get('is_success'):
            user['is_login'] = False
        else:
            user['is_login'] =  response.get('data').get('is_login')

    context = {
        'user': user
    }

    return render_template('index.html', context=context)


if __name__ == '__main__':
    app.debug = True
    # app.secret_key = 'N0GiuzUGHkrbfGRazAV2QgxAZy3AJWHd'
    app.run()
