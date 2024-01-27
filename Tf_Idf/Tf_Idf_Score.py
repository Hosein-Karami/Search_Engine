class Tf_Idf_Vector:

    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.tf_idf_weights = {}
        self.documents_square_sum = 0

    def set_square_sum(self, result):
        self.documents_square_sum = result
