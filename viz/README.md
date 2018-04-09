
Code partially based on http://karpathy.github.io/2015/05/21/rnn-effectiveness/ by @karpathy.

Steps:
------

1. `python server.py` from within `viz`. Defaults to port 8081, but it can be changed via the variable `PORT` in `server.py`.
2. From your script, console, jupyter notebook... (assuming `viz` is in your path), `from viz.client import register_data`.
3. `register_data(your_text, corresponding_scores)` where `corresponding_scores` can be:
   - 1D list of the same length as `your_text`
   - 2D list with dimensions (number of scores x length of text)
4. Browse to http://localhost:8081
