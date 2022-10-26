def get_uid(request):
    """return uid or None"""

    return request.cookies.get('uid')


def get_user(request):
    """return user or None"""
    import requests

    uid = get_uid(request)

    if not uid:
        return None

    response = requests.get(
        f'http://127.0.0.1:8000/users/{uid}').json()

    if not response.get('is_success'):
        return None

    return response['data']['user']
