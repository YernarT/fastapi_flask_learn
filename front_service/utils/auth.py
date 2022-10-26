def get_user(request):
    user = {}
    uid = request.cookies.get('uid')

    if uid is None:
        user['is_login'] = False
    else:
        import requests
        
        response = requests.get(
            f'http://127.0.0.1:8000/is_logged/{uid}').json()
        
        if not response.get('is_success'):
            user['is_login'] = False
        else:
            user['is_login'] =  response.get('data').get('is_login')

    return user