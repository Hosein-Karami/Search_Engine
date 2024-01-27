import threading

from Preprocess.Document_Positions import Document_Positions
from Preprocess.General_Tokenizer import General_Tokenizer


class Document_Tokenizer(General_Tokenizer):

    def __init__(self, deleted_most_frequent_count):
        self.deleted_most_frequent_count = deleted_most_frequent_count
        self.threads = []
        self.positions = []
        self.frequencies = {}
        self.mutex = threading.Lock()

    def start(self, text, doc_id):
        thread = threading.Thread(target=self.document_process, args=(text, doc_id,))
        self.threads.append(thread)
        thread.start()

    def document_process(self, text, doc_id):
        local_positions = self.process(text)
        document_positions = Document_Positions(doc_id, local_positions)
        self.positions.append(document_positions)
        self.update_frequencies(document_positions.positions)
        print(f'Tokenizer thread finished for doc with id = {doc_id}')

    def update_frequencies(self, positions):
        self.mutex.acquire()
        for word in positions.keys():
            if self.frequencies.get(word) is None:
                self.frequencies[word] = len(positions.get(word))
            else:
                self.frequencies[word] += len(positions.get(word))
        self.mutex.release()

    def wait(self):
        for thread in self.threads:
            thread.join()
        stop_words = self.show_most_frequent_words()
        return self.positions, self.frequencies, stop_words

    def show_most_frequent_words(self):
        targets = dict(sorted(self.frequencies.items(), key=lambda x: x[1], reverse=True)[:self.deleted_most_frequent_count])
        print(f'{self.deleted_most_frequent_count} words with most frequency in documents which should delete:')
        print(str(targets))
        return targets

    def get_positional_index(self):
        return self.positions
