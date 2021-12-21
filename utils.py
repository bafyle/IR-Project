from typing import Any, Iterable


def search(sorted_iterable: Iterable, search: Any) -> int:
    """
    Returns the index of the 'search' inside the 'sorted_iterable' 
    """
    low = 0
    high = len(sorted_iterable) - 1
    while low <= high:
        mid = (low + high) // 2
        guess = sorted_iterable[mid]
        if guess == search:
            return mid
        if guess > search:
            high = mid - 1
        else:
            low = mid + 1
    return None


import re
numbers = re.compile(r'(\d+)')

def numericalSort(value):
    """
    Numerical sorting function for sorting files in a numerical order.
    This function is used only and only for sorting files' names from glob
    """
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


custom_stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "from", "up", "down", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "very", "s", "t", "can", "will", "just", "don", "should", "now"]