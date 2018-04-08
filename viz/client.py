
import requests
import numpy as np

from .server import PORT


def register_data(text, scores, port=PORT):
    rtype = 'simple'

    if len(text) != len(scores):
        raise ValueError("Unequal lengths: {} != {}".format(
            len(text), len(scores)))

    if isinstance(scores[0], (list, np.ndarray)):
        rtype = 'mult'

    if isinstance(scores, np.ndarray):
        scores = scores.tolist()

    data = {'text': text, 'scores': scores, 'rtype': rtype}

    r = requests.post(
        'http://localhost:{}/register/'.format(PORT), json=data)

    return r.status_code == 200


if __name__ == '__main__':
    import lorem
    text = '\n'.join([lorem.sentence() for _ in range(10)])
    print(register_data(text, np.random.randn(len(text))))
