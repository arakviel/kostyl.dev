"""Спільні дані: корпус movie_reviews (NLTK), підготовка як у клітинці лекції 04."""
import random
from collections import Counter

import nltk
nltk.download("movie_reviews", quiet=True)
from nltk.corpus import movie_reviews

docs = [movie_reviews.words(fid) for fid in movie_reviews.fileids()]
all_words = [w.lower() for doc in docs for w in doc if any(c.isalpha() for c in w)]
freq = Counter(all_words)


def vocab_growth():
    random.seed(42)
    fileids = movie_reviews.fileids()
    random.shuffle(fileids)
    sizes = [10, 25, 50, 100, 200, 500, 1000, 2000]
    out = []
    for n in sizes:
        ws = [w.lower() for fid in fileids[:n] for w in movie_reviews.words(fid) if any(c.isalpha() for c in w)]
        out.append(len(set(ws)))
    return sizes, out
