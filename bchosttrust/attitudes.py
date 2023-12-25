# bchosttrust/bchosttrust/attitudes.py
"""Constants of the meanings of attitudes"""

from collections import defaultdict

UPVOTE = 0

WEIGHTS = defaultdict(lambda: 0)
WEIGHTS[UPVOTE] = 1
