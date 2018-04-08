
import torch
from torch.autograd import Variable


def rnn_input(model, seed):
    """
    Prepare input batch. Assumes dict has either <bos> & <eos>
    or only <eos> for linebreaks.
    """
    inp = []
    if model.embeddings.d.get_bos() is not None:
        inp.append(model.embeddings.d.get_bos())

    for i in seed:
        if i == '\n':
            if model.embeddings.d.get_eos() is not None:
                inp.append(model.embeddings.d.get_eos())
            if model.embeddings.d.get_bos() is not None:
                inp.append(model.embeddings.d.get_bos())
            else:
                continue
        elif i not in model.embeddings.d.s2i:
            print("Unknown symbol [{}]".format(i))
        inp.append(model.embeddings.d.index(i))

    return Variable(torch.LongTensor(inp).unsqueeze(1), volatile=True)


def rnn_input_text(model, inp):
    """
    Transform the rnn to text using the model's own dictionary
    """
    targets, d = [], model.embeddings.d
    eos, bos = d.get_eos(), d.get_bos()
    for i in inp:
        if eos is not None and i == eos:
            targets.append('\n')
        elif bos is not None and i == bos:
            continue
        else:
            targets.append(d.vocab[i])

    return targets


def get_next_probability(model, seed):
    """
    Get model's next step probability distribution
    """
    (*_, last), _, _ = model(rnn_input(model, seed))
    logprob = model.project(last)
    # unwrap variable
    logprob = logprob.data
    # remove singleton dimension
    logprob = logprob.squeeze(0)
    # transform to numpy array
    probs = logprob.exp().numpy()

    targets = model.embeddings.d.vocab
    return targets, probs


def generate_text(model, seed=None, length=100, temperature=1.0):
    """Generate text"""
    d = model.embeddings.d

    _, (text, *_) = model.generate(
        d, seed_texts=seed, temperature=temperature, max_seq_len=length,
        batch_size=1, ignore_eos=True)

    return ''.join([d.vocab[i] for i in text])


def stepwise_scores(model, text, score_entropy=False):
    """
    Compute stepwise scores (probabilities) over input sequence.
    If `score_entropy` is passed, the output will be the step entropy.
    """
    # run model
    inp = rnn_input(model, text)
    output, *_ = model(inp)
    logprobs = model.project(output)
    inp, logprobs = inp[1:].squeeze(1).data, logprobs[:-1].data

    # get target text
    targets = rnn_input_text(model, inp)

    # score
    if score_entropy:
        scores = -(logprobs.exp() * logprobs).sum(dim=1)
    else:
        scores = logprobs.gather(1, inp.unsqueeze(1)).exp()
        scores = scores.squeeze(1)

    return targets, scores.numpy()


def get_activations(model, text):
    """
    get last layer activations
    """
    inp = rnn_input(model, text)
    output, _, _ = model(inp)
    output = output.squeeze(1)       # remove batch dim
    output = output[:-1]             # remove extra activation
    output = output.transpose(0, 1)  # cell first
    output = output.data.numpy()

    inp = inp.squeeze(1).data[1:]
    targets = rnn_input_text(model, inp)

    return targets, output


# from seqmod.utils import load_model
# lm = load_model('./models/shakespeare-1.8850.pt')
# # idx, probs = stepwise_scores(lm, 'To be or not to be')
# output = get_activations(lm, 'To be or not to be ')
