import math
import threading


class Tf_Idf_Ranker:

    def __init__(self, documents_tf_idf, words_idf, positions, champions_list):
        self.words_idf = words_idf
        self.documents_tf_idf = documents_tf_idf
        self.positions = positions
        self.champions_list = champions_list
        self.threads = []
        self.scores = None

    def search(self, query_tokens):
        self.scores = {}
        query_weights = {}
        for word in self.words_idf.keys():
            if not ((word not in query_tokens) or (self.words_idf.get(word) == 0)):
                query_weights[word] = ((1 + math.log10(len(query_tokens.get(word)))) * (self.words_idf.get(word)))

        target_documents_list = []
        for query_token in query_tokens:
            champions = self.champions_list.get(query_token)
            if champions is not None:
                for doc in champions:
                    if doc not in target_documents_list:
                        target_documents_list.append(doc)

        query_squares_sum = 0
        for weight in query_weights.values():
            query_squares_sum += math.pow(weight, 2)
        query_squares_sum = math.sqrt(query_squares_sum)

        for document in target_documents_list:
            thread = threading.Thread(target=self.calculate_cosine_score, args=(query_weights, document, query_squares_sum,))
            self.threads.append(thread)
            thread.start()

    def calculate_cosine_score(self, query_weights, document, query_squares_sum):
        multiplying_sum = 0
        doc_word_weight = None
        for query_word in query_weights.keys():
            doc_word_weight = document.tf_idf_weights.get(query_word)
            if doc_word_weight is not None:
                multiplying_sum += query_weights.get(query_word) * doc_word_weight
        self.scores[document.doc_id] = multiplying_sum / (query_squares_sum * document.documents_square_sum)

    def wait(self):
        for thread in self.threads:
            thread.join()
        self.threads.clear()
        return self.scores
