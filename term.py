import math

class Term:
    """
    Term is a word with its postings list and frequency.
    The postings list is a dictionary, the key of the dictionary is the id of the document,
    the value of that key is list with all positions of this term in that document
    
    """
    documents_number: int


    def __init__(self, word: str = str(), postings_list: dict = None):
        self.word = word
        self.postings_list = postings_list
        self.frequency = len(self.postings_list) if postings_list != None else 0
        self.total_frequency = 0
        self.frequency_in_each_doc = dict()
        if postings_list is not None:
            for key in self.postings_list:
                self.total_frequency += len(self.postings_list[key])
                self.frequency_in_each_doc[key] = len(self.postings_list[key])
        self.IDF = math.log10(Term.documents_number/self.frequency)



    def get_TF_weight(self, document_id):
        """
        Return the Term Frequency weight in certain document

        Return 0 if the term is not in that document
        """
        if (tf := self.frequency_in_each_doc.get(document_id)) == None:
            return 0
        return 1 + math.log10(tf)
    

    def get_TF_IDF(self, document_id):
        """
        Return the TF IDF for certain document

        Return 0 If
        """
        # return 0 if self.get_TF_weight(document_id) == 0 else self.get_TF_weight(document_id) * self.IDF
        if self.frequency_in_each_doc.get(document_id) == None:
            return 0
        return self.get_TF_weight(document_id) * self.IDF

    
    def get_normalized_length(self, tfidf: list[float], document_id: int):
        return self.get_TF_IDF(document_id) / Term.get_length_using_tfidf(tfidf)


    def __eq__(self, __o: object) -> bool:
        """
        Equal operator overloading
        """
        if type(__o) == Term:
            return __o.word == self.word
        elif type(__o) == str:
            return __o == self.word


    def __str__(self) -> str:
        """
        __str__ returns a string when printing object of Term
        """
        return f"term: {self.word}, frequency: {self.frequency}, total frequency: {self.total_frequency}" \
                f" postings list: {self.postings_list}"


    def __lt__(self, __o) -> bool:
        """
        Less Than operator overloading, used for sorting and comparing
        """
        if type(__o) == Term:
            index = 0
            while len(self.word) > index < len(__o) and self.word[index] == __o.word[index]:
                index += 1
            if len(self.word) > index < len(__o.word):
                return ord(self.word[index]) < ord(__o.word[index])
            else:
                if len(self.word) < len(__o.word):
                    return True
                else:
                    return False
        elif type(__o) == str:
            index = 0
            while len(self.word) > index < len(__o) and self.word[index] == __o[index]:
                index += 1
            if len(self.word) > index < len(__o):
                return ord(self.word[index]) < ord(__o[index])
            else:
                if len(self.word) < len(__o):
                    return True
                else:
                    return False


    def __gt__(self, __o) -> bool:
        """
        Greater Than operator overloading, used for sorting and comparing
        """
        if type(__o) == Term:
            index = 0
            while len(self.word) > index < len(__o) and self.word[index] == __o.word[index]:
                index += 1
            if len(self.word) > index < len(__o.word):
                return ord(self.word[index]) > ord(__o.word[index])
            else:
                if len(self.word) > len(__o.word):
                    return True
                else:
                    return False
        elif type(__o) == str:
            index = 0
            while len(self.word) > index < len(__o) and self.word[index] == __o[index]:
                index += 1
            if len(self.word) > index < len(__o):
                return ord(self.word[index]) > ord(__o[index])
            else:
                if len(self.word) > len(__o):
                    return True
                else:
                    return False


    def __repr__(self) -> str:
        return self.__str__()


    @staticmethod
    def search_for_term(terms: list, term: str) -> int:
        low = 0
        high = len(terms) - 1
        while low <= high:
            mid = (low + high) // 2
            guess = terms[mid]
            if guess == term:
                return mid
            if guess > term:
                high = mid - 1
            else:
                low = mid + 1
        return None
    

    @staticmethod
    def get_length_using_tfidf(tfidf: list[float]):
        """Compute the length of a document by passing all TF.IDF values in that document """
        sqrt_number = 0
        for idf in tfidf:
            sqrt_number += idf ** 2
        return math.sqrt(sqrt_number)
