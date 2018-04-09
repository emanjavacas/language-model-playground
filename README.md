# Language Model Playground 
### in occassion of the Workshop "Asibot: under the hood" held at IoT Rotterdam, April 9. 2018.

Parts of this repository are inspired by/based on [A. Karpathy's blog post](http://karpathy.github.io/2015/05/21/rnn-effectiveness/) and [Y. Goldberg's reply post](http://nbviewer.jupyter.org/gist/yoavg/d76121dfde2618422139).

The goal of this repository is to provide code to play around with Language Model based text generation.
The entry is the IoT.ipynb jupyter notebook. Better structured code can be found in `ngram_lm.py` and `rnn_lm.py`.

- Dependencies: Python 3 (with Jupyter 4.4.0 support)
- Required packages: 
  - numpy=1.13.0
  - matplotlib=2.0.2
  - lorem
- Required packages for the RNN models:
  - seqmod: see [installation instructions](https://github.com/emanjavacas/seqmod/) and [requirements](https://github.com/emanjavacas/seqmod/blob/master/requirements.txt)
  - pytorch==0.3.1

# Visualizing RNN states over generated/processed text
See code inside `./viz` which should allow you to run the visualization shown below.

![viz](./img/viz-play.gif)
