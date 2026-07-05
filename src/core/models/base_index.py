class BaseIndex:
    def __init__(self):
        self.documents = {}

    def add_document(self, document):
        self.documents[document.doc_id] = document

    def get_document(self, doc_id):
        return self.documents.get(doc_id)

    def remove_document(self, doc_id):
        if doc_id in self.documents:
            del self.documents[doc_id]

    def list_documents(self):
        return list(self.documents.values())