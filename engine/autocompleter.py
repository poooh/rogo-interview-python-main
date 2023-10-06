import itertools

from typing import List

from .term_index import TermIndex, Term
from .nlp import Preprocessor

class Autocompleter:

    def __init__(self, term_index: TermIndex) -> None:
        self.term_index = term_index 

    def suggestions(self, text: str) -> List[List[Term]]:
        N = 3
        pp = Preprocessor(N)
        cleaned_input = pp.cleanup(text)
        ngrams = pp.ngram(cleaned_input)
        i = 0
        cross_terms = []
        while i < len(ngrams):
            grams = ngrams[i]
            flag = True
            for j, gram in enumerate(grams):
                terms = self.term_index.search(gram[1])
                # If we find a bigger match, jump ahead.
                if terms:
                    i += gram[0]
                    cross_terms.append(terms)
                    flag = False
                    break
            if flag:
                cross_terms.append([])
                i += 1
        if not cross_terms:
            return []

        return list(itertools.product(*cross_terms))
