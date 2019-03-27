
from collections import defaultdict, Counter
import numpy as np

from utils import entropy


PAD_TOKEN, EOS_TOKEN = '<pad>', '<eos>'


class UnsmoothedLM(object):

    """
    Learn MLE probability distributions from Ngram data

    Parameters:
    -----------

    - order: int, length of the ngram used to estimate the probability
        of the next token.
    """

    def __init__(self, order, pad_token=PAD_TOKEN):
        self.order = order
        self.pad_token = pad_token
        self.model = defaultdict(Counter)  # {('a', 'a', 'r', 'd'): {'v': 1.}}
        self.vocab = set()

    def fit(self, tokens):
        """
        - tokens: iterable over tokens (characters, words, etc..)
        """
        for *pref, target in ngrams(tokens, self.order + 1, self.pad_token):
            self.model[tuple(pref)][target] += 1
            self.vocab.add(target)  # keep track of vocabulary size

        # normalize to proper probability distributions
        for prefix, counter in self.model.items():
            total = sum(counter.values())
            self.model[prefix] = [(t, cnt/total) for t, cnt in counter.items()]

        return self

    def _generate_next(self, prefix, temperature=1.0):
        if len(prefix) < self.order:
            raise ValueError("Needs at least prefix of length {}".format(self.order))

        # chop off to model order
        prefix = prefix[-self.order:]
        try:
            targets, probs = zip(*self.model[tuple(prefix)])
            sampled = np.random.multinomial(1, np.array(probs), 1).argmax()
            return targets[sampled]
        except:
            raise ValueError("Unknown prefix {}".format(''.join(prefix)))

    def generate_text(self, seed=None, length=100, temperature=1.0):
        """
        - seed: iterable of tokens to use as seed to start generating
        - length: int, max number of tokens to be generated
        - temperature: float (1, -), flattening factor for the output distribution
        """
        if seed is None:
            seed = [self.pad_token] * self.order  # start from first token (f)

        output = ''
        for _ in range(length):
            new = self._generate_next(seed, temperature=temperature)
            seed = seed[1:] + [new]
            output += new

        return output

    @staticmethod
    def apply_temperature(probs, tau):
        """
        Apply temperature and renormalize to output distribution
        """
        # new_probs = np.log(probs) / tau
        # exped = np.exp(new_probs)
        # return exped / exped.sum()
        new_probs = probs ** (1 / tau)
        return new_probs / new_probs.sum()

    def get_probabilities(self, text, score_entropy=False):
        """
        Compute stepwise scores (probabilities) over input sequence.
        If `score_entropy` is passed, the output will be the step entropy.
        """
        scores, targets = [], []
        skips = 0

        for *prefix, target in ngrams(text, self.order + 1, self.pad_token):
            if skips < self.order:  # skip padding items at the beginning
                skips += 1
                continue

            try:
                dist = dict(self.model[tuple(prefix)])
                targets.append(target)
                if score_entropy:
                    _, probs = zip(*dist.items())
                    scores.append(entropy(probs, len(self.vocab)))
                else:
                    scores.append(dist[target])

            except ValueError:  # too many values to unpack => OOV
                raise ValueError("Couldn't find estimate for prefix [{}]".format(prefix))

        return targets, scores


def ngrams(items, ngram_order, pad_token=PAD_TOKEN):
    """
    Memory efficient ngram function
    """
    buf = []

    for it in items:
        buf.append(it)

        if len(buf) == ngram_order:
            yield tuple(buf)
            buf.pop(0)
        else:
            yield tuple([pad_token] * (ngram_order - len(buf)) + buf)


def characters_from_files(*files):
    for f in files:
        with open(f, 'r') as f:
            for line in f:
                for c in line:
                    yield c


def words_from_files(*files, eos_token=EOS_TOKEN):
    for f in files:
        with open(f, 'r') as f:
            for line in f:
                for w in line.split():
                    yield w
                yield eos_token
