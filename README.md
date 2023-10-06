# rogo-interview-python

## Instructions

We challenge you to build an autocomplete function similar to what Rogo has under the hood.

We've provided you with a term index that takes in a string prefix and returns a list of matching terms. For example, if you query the term index with "m", you'll get the following terms back in response: [median], [maximum], [minimum], [microsoft inc]. You can think of the term index as an in-memory implementation of an Elasticsearch index. You can look at this class in `engine/term_index.py` to see what it does, but you can't make any modifications to it.

Your task is to implement a Python algorithm that inputs a string and returns matching queries. A input string might match 0, 1, or many queries. Each query contains 1 or more terms. The order the queries are returned in doesn't matter.

The scaffolding code has been provided in `engine/autocompleter.py`. Your goal is to make the unit tests pass (`tests/test_autocomplete.py`) by completing this class's implementation. You're not allowed to use any external libraries, and you must come up with the solution by yourself (no LLMs!). Produce Python 3 code that is as clean and idiomatic as you find appropriate, and leverage Python typing where it's useful.

During the interview, you'll have the opportunity to present your solution, explain your thought process and the logic behind it.

Good luck!


## Examples

```
Input: "app"
Output: 
  - [apple]

Input: "apple revenue by month"
Output: 
  - [apple] [revenue] [by month]

Input: "apple revenue by month last 12 "
Output:     
  - [apple] [revenue] [by month] [last 12 months]
  - [apple] [revenue] [by month] [last 12 years]
```

(You can find more examples in the unit test file)

__Tip: Terms in this exercise will never exceed 3 words, so you can build that assumption into your algorithm.__

## Solution

The solution involves 4 steps:
* Cleanup: This step contains removal of punctuations. More steps can be added to it in future via the json and adding functions.
* ngrams: We get ngrams(unigrams, bigrams, trigrams, etc) at each index. Currently, we get max trigrams. 
* Matching: For each index, we match the highest gram first. If we find a match, we skip those many indices and repeat the search. For eg: if we find a trigram match at index 2, we skip 3 indices and repeat search from index 5. We save all the list of search terms at different indices.
* Cartesian product: We get a cartesian product of the list we get from previous step and return.

### Example:

```
Input: "mi ebit by month 2023"
```
Output after each steps:

* Cleanup:
```
Output: "mi ebit by month 2023"
```

* ngrams:
```
Output: [[(3, "mi ebit by"), (2, "mi ebit"), (1, "mi")],
         [(3, "ebit by month"), (2, "ebit by"), (1, "ebit")],
         [(3, "by month 2023"), (2, "by month"), (1, "by")],
         [(2, "month 2023"), (1, "month")],
         [(1, "2023")]]
```
At index 0, we get a trigram("mi ebit by"), a bigram("mi ebit") and a unigram("mi").
And so on.

* Matching:
```
Output: [[Term(value='microsoft'), Term(value='minimum')],
         [Term(value='ebit'), Term(value='ebitda')],
         [Term(value='by month')],
         [Term(value='2023')]]
```
At index 0, we get a search match of unigram "mi" with "microsoft" and "minimum".
Becuase it's a unigram match, we skip 1 index and at index 1, we get a search match of unigram "ebit" with "ebit" and "ebitda".
We skip 1 and at index 2, we get a search match of bigram "by month" with "by month".
We skip 2 and finally at index 4, we get a search match of unigram "2023" with "2023".

* Cartesian product: 
```
Output: [['microsoft', 'ebit', 'by month', '2023'],
         ['microsoft', 'ebitda', 'by month', '2023'],
         ['minimum', 'ebit', 'by month', '2023'], 
         ['minimum', 'ebitda', 'by month', '2023']]
```