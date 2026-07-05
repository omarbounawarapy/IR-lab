class Document:
    def __init__(self, doc_id: str, content: str, metadata: dict = None):
        self.doc_id = doc_id
        self.content = content
        self.metadata = metadata if metadata is not None else {}

    def __repr__(self):
        return f"Document(doc_id={self.doc_id}, content={self.content}, metadata={self.metadata})"                                                    
