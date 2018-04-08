
import json
import uuid
from random import randint

import bottle
from bottle import route, run, request, response, template, static_file

bottle.BaseRequest.MEMFILE_MAX = int(1e+8)  # allow large objects to be posted (100MB)

PORT = 8081

global DATA

DATA = {
    # identify if new data has been pushed from python
    'token': None,
    # global text data
    'text': None,
    # global score data (list of lists)
    'scores': None,
    # mult or simple (multiple scores per token or just one)
    'rtype': None,
    # in case of `mult` rtype, store the current pointer
    'pointer': 0
}


def get_payload():
    payload = {}
    for key, val in DATA.items():
        if key == 'scores':
            if DATA['rtype'] == 'mult':
                payload[key] = val[DATA['pointer']]
            else:
                payload[key] = val
        else:
            payload[key] = val

    return payload


@route('/')
def index():
    return template("index.tpl", msg="Nothing registered yet!", port=PORT)


@route('/static/<filepath>')
def static(filepath):
    return static_file(filepath, root="static")


# coming from python
@route('/register/', method=['POST'])
def register():
    try:
        DATA['text'] = request.json['text']
        DATA['scores'] = request.json['scores']
        DATA['token'] = str(uuid.uuid1())
        DATA['rtype'] = request.json['rtype']
        response.status = 200
        return

    except Exception as e:
        response.status = 400
        return


# coming from client
@route('/poll/')
def poll():
    token = request.params.get('token', None)
    if DATA.get('token') is not None and (token is None or token != DATA['token']):
        return json.dumps({"status": True, **get_payload()})
    else:
        return json.dumps({"status": False})


def only_rtype(rtype):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            if DATA['rtype'] != rtype:
                return json.dumps({"status": False})
            return func(*args, **kwargs)
        return wrapped
    return wrapper


@only_rtype('mult')
@route('/next/')
def next():
    DATA['pointer'] = (DATA['pointer'] + 1) % len(DATA['scores'])
    return json.dumps({"status": True, **get_payload()})


@only_rtype('mult')
@route('/prev/')
def prev():
    DATA['pointer'] = (DATA['pointer'] - 1) % len(DATA['scores'])
    return json.dumps({"status": True, **get_payload()})


@only_rtype('mult')
@route('/random/')
def random():
    DATA['pointer'] = randint(0, len(DATA['scores']) - 1)
    return json.dumps({"status": True, **get_payload()})


@only_rtype('mult')
@route('/getcell/')
def getcell():
    cell_num = int(request.params.get('pointer', DATA['pointer']))
    if cell_num > 0 and cell_num < len(DATA['scores']):
        DATA['pointer'] = cell_num
        return json.dumps({"status": True, **get_payload()})
    return json.dumps({"status": False})


if __name__ == '__main__':
    run(host='localhost', port=PORT)
