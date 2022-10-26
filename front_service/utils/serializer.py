def obj_to_json(_obj):
    from json import dumps
    return dumps(_obj)


def json_to_obj(_json):
    from json import loads
    return loads(_json)
