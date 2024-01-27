class Positional_Index:

    def __init__(self, frequency):
        self.frequency = frequency
        self.positions = {}

    def add_positions(self, doc_id, positions):
        self.positions[doc_id] = positions
