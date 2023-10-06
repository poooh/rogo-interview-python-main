import string

from typing import List


class Preprocessor(object):
    def __init__(self, n: int):
        self.n = n

    def ngram(self, text: str) -> List[str]:
        splits = text.split()
        ngrams = [[] for s in splits]
        for i in range(self.n, 0, -1):
            for j in range(len(splits) - i + 1):
                ngrams[j].append((i, " ".join(splits[j: j + i])))
        return ngrams

    @staticmethod
    def cleanup(text: str) -> str:
        # Remove punctuations
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Add more cleanup processes like stopword removal/etc when required
        return text.strip()
