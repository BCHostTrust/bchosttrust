# bchosttrust/bchosttrust/attitudes.py
# Constants of the meanings of attitudes

from collections import defaultdict

UPVOTE = 0
DOWNVOTE = 1

WEIGHTS = defaultdict(lambda: 0)
WEIGHTS[UPVOTE] = 1
WEIGHTS[DOWNVOTE] = -1
