import math
from typing import List

import glob
from term import Term
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

############## Part 1 ##############

def remove_stop_words(words: List[str]):
    """
    Removes the stop words from a list of words OUTPLACE
    """
    stop_words = stopwords.words("english")
    for index, word in enumerate(words):
        if word in stop_words:
            words.pop(index)
    return words

def remove_punc(words: List[str]):
    """
    Removes all punctuation from a list of tokens OUTPLACE
    """
    return [w for w in words if w.isalnum()]


def query_optimization(query: str) -> list:
    return remove_punc(remove_stop_words(word_tokenize(query)))

def convert_documents_to_tokens() -> dict:
    """
    Returns dictionary, each key in it is a document ID and the value for each key is
    a list with all tokens inside that document

    All preprocessing is applied
    """
    ## Specifying the number of all documents
    doc_id = 0
    documents_tokens = dict()

    ## build a list of all files' name from 'default files' and 'files' directories
    custom_documents = glob.glob(r'.\files\*')
    default_documents = glob.glob(r'.\default files\*')
    # load default documents if custom documents is empty (files directory is empty)
    documents = custom_documents if len(custom_documents) > 0 else default_documents

    # set documents number
    Term.documents_number = len(documents)

    for document_name in documents:
        with open(document_name, 'r') as document:
            lines = list(map(str.lower, map(str.strip, document.readlines())))
            for line in lines:
                tokens_in_one_line = remove_punc(remove_stop_words(word_tokenize(line)))
                if documents_tokens.get(doc_id) == None:
                    documents_tokens[doc_id] = tokens_in_one_line
                else:
                    documents_tokens[doc_id] += tokens_in_one_line
            doc_id += 1

    ## documents_tokens should be full of all words in the files
    # print(documents_tokens)
    return documents_tokens


############## Part 2 ##############

def get_distincit_tokens(documents_tokens):
    """
    Return a sorted list with all distinct tokens
    """
    tokens_set = set()
    for tokens in documents_tokens.values():
        tokens_set.update(tokens)
    tokens_set = sorted(tokens_set)
    ## distinct tokens set should be sorted in ascending order
    # print(tokens_set)
    return tokens_set

def build_terms(documents_tokens):
    """
    Return a list of terms from all tokens that is brought from the documents collection
    """
    tokens_set = get_distincit_tokens(documents_tokens)
    
    terms = list()
    for distinct_token in tokens_set:
        term_postings_list = dict()
        for document_index, tokens in enumerate(documents_tokens.values()):
            for token_index, token in enumerate(tokens, 1):
                if token == distinct_token:
                    if term_postings_list.get(document_index) == None:
                        term_postings_list[document_index] = [token_index]
                    else:
                        term_postings_list[document_index] += [token_index]
        terms.append(Term(distinct_token, term_postings_list))
    return terms


def apply_query_on_documents(query: List[str], terms: List[Term]) -> List:
    """
    Apply a query on the documents and return a dictionary with all documents that contain the query
    and their position
    e.g: {0: [3, 9], 2:[15, 998], ....}
    """
    ## Search for query in terms list
    indices = list()
    for term in query:
        indices.append(Term.search_for_term(terms, term))
    indices.sort(key=lambda x: len(terms[x].postings_list))
    
    results = dict()

    post1 = terms[indices[0]].postings_list
    indices.pop(0)
    post2 = terms[indices[0]].postings_list
    
    while len(indices) :
        post2 = terms[indices[0]].postings_list
        for key, post1_value in post1.items():
            if key in post2:
                positions = []
                post2_value = post2[key]
                for i in post1_value:
                    for f in post2_value:
                        if abs(i-f) == 1:
                            positions.append(max(i, f))
                results[key] = positions
        post1 = results
        indices.pop(0)

    return results

############## Part 3 ##############

def display_TF_IDF_matrix(terms):
    """
    Displays the TF.IDF Matrix for all terms in terminal or console
    """
    header = "\t\t\t\t"
    for i in range(10):
        header += f'Doc{i+1}\t'
    print(header)
    for term in terms:
        row = f"Term: {term.word}\t\t\t"
        for i in range(10):
            row += f"{term.get_TF_IDF(i):.2f}\t"
        print(row)


def compute_documents_lengths(terms: list, number_of_documents: int) -> list:
    """
    Returns a list with all documents' length
    """
    output = list()
    index = 0
    while index < number_of_documents:
        sum_of_idfs_square = 0
        for term in terms:
            sum_of_idfs_square += (term.get_TF_IDF(index))**2
        output.append(math.sqrt(sum_of_idfs_square))
        index += 1
    return output

def compute_similarity(document_ID, query_terms, terms) -> float:
    tfidfs = list()
    for term in terms:
        tfidfs.append(term.get_TF_IDF(document_ID))
    output = 0
    for key in query_terms:
        output = query_terms[key]['normalized'] * terms[Term.search_for_term(terms, key)].get_normalized_length(tfidfs, document_ID)
    return output

if __name__ == "__main__":
    
    terms = build_terms(convert_documents_to_tokens())
    documents_query = "text messages"
    documents_query_tokens = query_optimization(documents_query)
    print(apply_query_on_documents(documents_query_tokens, terms))


    similarity_query = "messages cairo"
    similarity_query_tokens = query_optimization(similarity_query)
    documents_lengths = compute_documents_lengths(terms, Term.documents_number)
    similarity_query_terms = dict()
    for query_token in similarity_query_tokens:
        similarity_query_terms[query_token] = {'tf': 1, 'tf_weight': 1, 'idf': terms[Term.search_for_term(terms, query_token)].IDF, 'df': terms[Term.search_for_term(terms, query_token)].frequency}

    sum_of_query_IDFS = 0
    for value in similarity_query_terms.values():
        value['tf_idf'] = value['tf_weight'] * math.log10(Term.documents_number/value['df'])
        sum_of_query_IDFS += value['tf_idf'] ** 2

    query_length = math.sqrt(sum_of_query_IDFS)

    for value in similarity_query_terms.values():
        value['normalized'] = value['idf'] / query_length



    # for i in range(10):
    #     print(compute_similarity(i, query_terms, terms))




    # display_TF_IDF_matrix(terms)

    # query = "business cairo university"
    # matched_docs = query_on_documents(word_tokenize(query_optimization(query)), terms)
    # print(matched_docs)