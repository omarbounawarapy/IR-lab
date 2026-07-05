class InvertedIndexer:
    def __init__(self):
        self.index = {}

    def add_document(self, document):
        for term in document.content.split():
            if term not in self.index:
                self.index[term] = {
                    "frequency": 0,
                    "documents": set()
                }
            self.index[term]["frequency"] += 1
            self.index[term]["documents"].add(document.doc_id)

    def get_documents(self, term):
        return self.index.get(term, {"frequency": 0, "documents": set()})
    