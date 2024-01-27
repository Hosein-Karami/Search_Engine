import heapq
import math
import threading

from Tf_Idf.Tf_Idf_Score import Tf_Idf_Vector


class Tf_Idf_Maker:

    def __init__(self, positional_index, docs_info):
        self.positional_index = positional_index
        self.docs_info = docs_info
        self.threads = []
        self.words_idf = {}
        self.documents_tf_idf = []
        self.champions_list = {}
        self.k_champion = 10

    def start(self):
        self.calculate_idf()
        for doc_info in self.docs_info:
            thread = threading.Thread(target=self.process, args=(doc_info.doc_id, doc_info.positions))
            self.threads.append(thread)
            thread.start()

    def calculate_idf(self):
        documents_count = len(self.docs_info)
        for word in self.positional_index.keys():
            self.words_idf[word] = math.log10(documents_count / len(self.positional_index.get(word).positions.keys()))

    def process(self, doc_id, positions):
        document_tf_idf = Tf_Idf_Vector(doc_id)
        word_positions = None
        for word in self.positional_index.keys():
            word_positions = positions.get(word)
            if not ((word_positions is None) or (self.words_idf.get(word) == 0)):
                document_tf_idf.tf_idf_weights[word] = ((1 + math.log10(len(word_positions))) * (self.words_idf.get(word)))

        result = 0
        for weight in document_tf_idf.tf_idf_weights.values():
            result += math.pow(weight, 2)
        document_tf_idf.set_square_sum(math.sqrt(result))

        self.documents_tf_idf.append(document_tf_idf)
        print(f'tf_idf weights was made for document with id : {doc_id}')

    def calculate_champions_list(self):
        champions_threads = []
        for word in self.words_idf.keys():
            thread = threading.Thread(target=self.calculate_champion_thread, args=(word,))
            champions_threads.append(thread)
            thread.start()
        for thread in champions_threads:
            thread.join()

    def calculate_champion_thread(self, word):
        temp_weights = {}
        for doc_tf_idf in self.documents_tf_idf:
            score = doc_tf_idf.tf_idf_weights.get(word)
            if score is not None:
                temp_weights[doc_tf_idf] = score
        temp_champions = heapq.nlargest(self.k_champion, temp_weights.items(), key=lambda i: i[1])
        champions = []
        for temp_champion in temp_champions:
            champions.append(temp_champion[0])
        self.champions_list[word] = champions
        print(f'champion list was made for {word}')

    def wait(self):
        for thread in self.threads:
            thread.join()
        self.calculate_champions_list()
        return self.documents_tf_idf, self.words_idf, self.champions_list
