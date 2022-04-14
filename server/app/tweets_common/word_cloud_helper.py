import re

import nltk
import numpy as np

from . import STOP_WORDS

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


def remove_emojis(data: str):
    return re.sub(emoj_regex, "", data)


def word_tokenize_nepali(text: str):
    text = remove_emojis(text)
    text = re.sub(r"\d+", " ", text)  # remove any digits
    text = re.sub(r"[,)({}[\]\.:;`_–\-``!‘’''“”?\-।/—%\|]+", " ", text)
    text = re.sub(
        r"\s+", " ", text
    )  # replace multiple whitespaces with single whitespace
    text = text.replace("#", "").replace(
        "_", " "
    )  # remove #, and break words containing underscore
    text_tokens = [
        token for token in nltk.tokenize.word_tokenize(text) if token not in STOP_WORDS
    ]
    return np.array(text_tokens)
