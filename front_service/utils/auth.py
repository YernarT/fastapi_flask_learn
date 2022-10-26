def get_uid(request):
    """return `uid` or `None`"""

    return request.cookies.get('uid')


def get_user(request):
    """return `user` or `fallback_user`"""
    import requests
    
    fallback_user = { 'is_login': False }
    uid = get_uid(request)

    if not uid:
        return fallback_user

    response = requests.get(
        f'http://127.0.0.1:8000/users/{uid}').json()

    if not response.get('is_success'):
        return fallback_user

    return response['data']['user']
