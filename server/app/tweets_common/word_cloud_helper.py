import re
from typing import List, Tuple

from nltk import FreqDist
from nltk.tokenize import word_tokenize

from . import STOP_WORDS
from .decorators import timed_lru_cache

emoj_regex = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002500-\U00002BEF"  # chinese char
    "\U00002702-\U000027B0"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"  # dingbats
    "\u3030"
    "]+",
    re.UNICODE,
)


def word_tokenize_nepali(text: str):
    # Remove emojis
    text = re.sub(emoj_regex, "", text)

    text = re.sub(r"\d+", " ", text)  # remove any digits
    text = re.sub(r"[,)({}[\]\.:;`_–\-``!‘’''“”?\-।/—%\|]+", " ", text)
    text = re.sub(
        r"\s+", " ", text
    )  # replace multiple whitespaces with single whitespace
    text = text.replace("#", "").replace(
        "_", " "
    )  # remove #, and break words containing underscore
    return tuple(token for token in word_tokenize(text) if token not in STOP_WORDS)


# cache 64 different results for half-a-day
@timed_lru_cache(seconds=43200, maxsize=64)
def get_word_count_distribution(tweets: Tuple[str]):
    """
    Get the word-count distribution from a tuple of tweets.
    Here tweets is a tuple, this is hashable while caching.
    """

    # It is a generator of tuples
    two_dimensional_tokens = map(word_tokenize_nepali, tweets)

    flat_tokens: List[str] = []

    for token in two_dimensional_tokens:
        flat_tokens.extend(token)

    word_freq = FreqDist(flat_tokens)

    return word_freq.most_common(100)
