class IncidenceMatrixIndexer:
    def index(self, docs: list[AnalyzedDocument]):

        vocabulary = {}
        matrix = []

        for doc_id, doc in enumerate(docs):
            for token in set(doc.tokens):

                if token not in vocabulary:
                    vocabulary[token] = len(vocabulary)
                    matrix.append([0] * len(docs))

                row = vocabulary[token]
                matrix[row][doc_id] = 1

        return matrix