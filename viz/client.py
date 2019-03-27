
import requests
import numpy as np

from .server import PORT


def _check_lengths(text, scores, rtype):
    _error = None
    if rtype == 'simple':
        if len(text) != len(scores):
            _error = "Unequal lengths: {} != {}".format(len(text), len(scores))
    else:
        for idx, s in enumerate(scores):
            if len(text) != len(s):
                _error = "Unequal lengths: {} != {} at pos {}".format(
                    len(text), len(s), idx)
                break
    if _error is not None:
        raise ValueError(_error)


def post_request(data, url='http://localhost:{}/register/', port=PORT):
    return requests.post(url.format(PORT), json=data, stream=True)


def register_data(text, scores, word=False, port=PORT):
    rtype = 'simple'

    if isinstance(scores[0], (list, np.ndarray)):
        rtype = 'mult'

    if isinstance(scores, np.ndarray):
        scores = scores.tolist()

    _check_lengths(text, scores, rtype)

    r = post_request(
        {'text': text, 'scores': scores, 'rtype': rtype, 'word': word},
        port=port)

    return r.status_code == 200


if __name__ == '__main__':
    import lorem
    text = '\n'.join([lorem.sentence() for _ in range(10)])
    print(register_data(text, np.random.randn(len(text))))
