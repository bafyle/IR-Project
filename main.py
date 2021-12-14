import math
from typing import Dict, List

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
    """
    return a list of all tokens in the query after preprocessing
    """
    return remove_punc(remove_stop_words(word_tokenize(query.strip().lower())))


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
    custom_documents = glob.glob(r'files/*.txt')
    default_documents = glob.glob(r'default files/*.txt')
    
    # load default documents if custom documents is empty (files directory is empty)
    if len(custom_documents) > 0:
        print("loading all documents in files/")
        documents = custom_documents
    else:
        print("loading all default documents")
        documents = default_documents
    
    # set documents number
    Term.documents_number = len(documents)

    for _, document_name in enumerate(documents):
        print(f"Document id {_} is: {document_name}")
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

def build_terms(documents_tokens) -> list[Term]:
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


def display_terms(terms: list[Term]):
    """
    Displays all terms in the same structure as asked in the project requirements PDF
    """
    for term in terms:
        row = f"{term.word}, {term.frequency}\n"
        for document, positions in term.postings_list.items():
            row +=f"{document}: {positions}\n"
        print(row)


def apply_query_on_documents(query: List[str], terms: List[Term]) -> Dict:
    """
    Apply a query on the documents and return a dictionary with all documents that contain the query
    and their position
    e.g: {0: [3, 9], 2:[15, 998], ....}
    """
    ## Search for query in terms list
    indices = list()
    for term in query:
        index = Term.search_for_term(terms, term)
        if index is not None:
            indices.append(index)
    indices.sort(key=lambda x: len(terms[x].postings_list))
    
    results = dict()
    if len(indices) >= 2:
        post1 = terms[indices[0]].postings_list
        indices.pop(0)
        while len(indices):
            post2 = terms[indices[0]].postings_list
            post1_keys = [key for key in post1]
            post2_keys = [key for key in post2]
            while min(len(post1_keys), len(post2_keys)) != 0:
                if post1_keys[0] == post2_keys[0]:
                    positions_list = list()
                    positions1 = post1[post1_keys[0]]
                    positions2 = post2[post2_keys[0]]
                    while min(len(positions1), len(positions2)) != 0:
                        if positions2[0] - positions1[0] == 1:
                            positions_list.append(positions2[0])
                            positions1.pop(0)
                            positions2.pop(0)
                        else:
                            if positions1[0] < positions2[0]:
                                positions1.pop(0)
                            else:
                                positions2.pop(0)
                    if any(positions_list):
                        results[post1_keys[0]] = positions_list
                    post1_keys.pop(0)
                    post2_keys.pop(0)
                else:
                    if post1_keys[0] < post2_keys[0]:
                        post1_keys.pop(0)
                    else:
                        post2_keys.pop(0)
            indices.pop(0)
    else:
        if len(indices) == 1:
            results = terms[indices[0]].postings_list
        else:
            results = {}

    
    # if len(indices) >= 2:
    #     post1 = terms[indices[0]].postings_list
    #     indices.pop(0)
    #     while len(indices):
    #         post2 = terms[indices[0]].postings_list
    #         for key, post1_value in post1.items():
    #             for key2, post2_value in post2.items():
    #                 if key == key2:
    #                     positions1 = []
    #                     for i in post1_value:
    #                         for f in post2_value:
    #                             if abs(i-f) == 1:
    #                                 positions1.append(max(i, f))
    #                     if any(positions1):
    #                         results[key] = positions1
    #             if key in post2:
    #                 pass   
    #         post1 = results
    #         indices.pop(0)
    # else:
    #     if len(indices) == 1:
    #         results = terms[indices[0]].postings_list
    #     else:
    #         results = {}
    return results

############## Part 3 ##############

def display_TF_IDF_matrix(terms):
    """
    Displays the TF.IDF Matrix for all terms in terminal or console
    """
    header = "\t\t\t\t"
    for i in range(10):
        header += f'Doc{i}\t'
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
    """
    This function computes the similarity between a query and a document
    """
    tfidfs = list() # list of all TF.IDF of all terms for that document
    for term in terms:
        tfidfs.append(term.get_TF_IDF(document_ID))
    

    output = 0 # output will be equal to the sum of product of all normalized values in the query with all terms' normalized values for that document
    for key in query_terms:
        output += query_terms[key]['normalized'] * terms[Term.search_for_term(terms, key)].get_normalized_length(tfidfs, document_ID)
    return output

if __name__ == "__main__":
    
    terms = build_terms(convert_documents_to_tokens())

    display_terms(terms)
    
    query = "example search"
    query_tokens = query_optimization(query)
    print(f"Query: {query_tokens}")
    docs_matched = apply_query_on_documents(query_tokens, terms)
    print(f"documents matched: {docs_matched}")

    if len(docs_matched) > 0:
        # Display TF.IDF matrix
        
        display_TF_IDF_matrix(terms)
        documents_lengths = compute_documents_lengths(terms, Term.documents_number)

        # compute similarities with the query and all documents
        """
            Calculating the similarities require term frequency and its weight, IDF, TF.IDF and the term frequency in all documents (DF)
            - The TF and TF weight in all tokens in the query are 1
            - The IDF value of the query token is the same as the document term
               we just searched for the term in the list of terms, grabbed the IDF value from it and
               set it to query token IDF
            - Document frequency is the same for this term in all of documents
        """
        # Building the structure of the tokens from the query
        similarity_query_terms = dict()
        for query_token in query_tokens:
            similarity_query_terms[query_token] = {'tf': 1, 'tf_weight': 1, 'idf': terms[Term.search_for_term(terms, query_token)].IDF, 'df': terms[Term.search_for_term(terms, query_token)].frequency}

        # Calculating the query length
        sum_of_query_IDFS = 0
        for value in similarity_query_terms.values():
            value['tf_idf'] = value['tf_weight'] * math.log10(Term.documents_number/value['df'])
            sum_of_query_IDFS += value['tf_idf'] ** 2
        query_length = math.sqrt(sum_of_query_IDFS)

        # Calculating the normalized TF.IDF weight, which is equal to TF.IDF / query length
        for value in similarity_query_terms.values():
            value['normalized'] = value['tf_idf'] / query_length

        # Sorting and calculating the similarities between all documents and the query
        document_similarities = dict()
        for i in range(Term.documents_number):
            document_similarities[i] = compute_similarity(i, similarity_query_terms, terms)
        sorted_document_similarities_indices = sorted(document_similarities, key=lambda x: document_similarities[x], reverse=True)
        
        for i in range(Term.documents_number):
            print(f"Similarity between the query and document number {sorted_document_similarities_indices[i]} is {document_similarities.get(sorted_document_similarities_indices[i])}")
        
