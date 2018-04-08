
import json
import uuid

from bottle import route, run, request, response, template
from bottle import static_file

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
    'rtype': None
}


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
        data = request.json
        DATA['text'] = data['text']
        DATA['scores'] = data['scores']
        DATA['token'] = str(uuid.uuid1())
        DATA['rtype'] = data['rtype']
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
        return json.dumps({"status": True, **DATA})
    else:
        return json.dumps({"status": False})


@route('/next/')
def next():
    pass


@route('/prev/')
def prev():
    pass


if __name__ == '__main__':
    run(host='localhost', port=PORT)
