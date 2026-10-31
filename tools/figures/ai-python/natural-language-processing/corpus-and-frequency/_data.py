"""Спільні дані: частоти слів у корпусі movie_reviews (NLTK)."""
import random
from collections import Counter
from nltk.corpus import movie_reviews, stopwords

words = [w for w in movie_reviews.words() if w.isalpha()]
counts = Counter(words)
stop = set(stopwords.words("english"))
