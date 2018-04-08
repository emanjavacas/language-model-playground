
import numpy as np
import matplotlib.pyplot as plt


def plot_output(targets, probs, prefix):
    # sort alphabetically
    targets, probs = zip(*sorted(zip(targets, probs), key=lambda t: t[0]))
    # transform into array
    probs = np.array(probs)

    fig = plt.figure(figsize=(16, 4))
    x = np.arange(len(targets))
    plt.bar(x, probs)
    plt.title(''.join(prefix))
    plt.xticks(x, targets)
    plt.yticks(np.linspace(0, 1, 9))
    plt.show()


def entropy(probs, vocab_size):
    probs = np.array(probs)
    if len(probs) < vocab_size:
        probs = np.concatenate([probs, np.zeros(vocab_size - len(probs)) + 1e-6], axis=0)
    return -(probs * np.log(probs)).sum(axis=0)
