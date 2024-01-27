from Index.Positional_Index import Positional_Index


class Indexer:

    def __init__(self, positions, stop_words, frequencies):
        self.positions = positions
        self.stop_words = stop_words
        self.frequencies = frequencies
        self.positional_index = {}

    def start(self):
        self.positions.sort(key=lambda x: x.doc_id, reverse=False)

        for position in self.positions:
            doc_positions = position.positions
            for word in doc_positions.keys():
                if word not in self.stop_words:
                    word_positions = self.positional_index.get(word)
                    if word_positions is None:
                        pos_index = Positional_Index(self.frequencies.get(word))
                        pos_index.add_positions(position.doc_id, doc_positions.get(word))
                        self.positional_index[word] = pos_index
                    else:
                        word_positions.add_positions(position.doc_id, doc_positions.get(word))

        self.positional_index = {key: value for key, value in sorted(self.positional_index.items())}

        return self.positional_index
