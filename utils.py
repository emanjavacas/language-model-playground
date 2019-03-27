
import numpy as np
import matplotlib.pyplot as plt


def plot_output(targets, probs, prefix):
    # sort alphabetically
    targets, probs = zip(*sorted(zip(targets, probs), key=lambda tup: tup[0]))
    # transform into array
    probs = np.array(probs)
    x = np.arange(len(targets))

    fig = plt.figure(figsize=(16, 4))
    ax = fig.add_subplot(111)
    ax.bar(x, probs)
    ax.set_title("History: '{}'".format("".join(prefix)))
    ax.set_xticks(x)
    ax.set_xticklabels(targets)
    ax.set_yticks(np.linspace(0, 1, 9))

    return ax


def entropy(probs, vocab_size):
    probs = np.array(probs)
    if len(probs) < vocab_size:
        probs = np.concatenate([probs, np.zeros(vocab_size - len(probs)) + 1e-6], axis=0)
    return -(probs * np.log(probs)).sum(axis=0)
