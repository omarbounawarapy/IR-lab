class Document:
    def __init__(self, id: str, content: str, metadata: dict = None):
        self.id = id
        self.content = content
        self.metadata = metadata if metadata is not None else {}

    def __repr__(self):
        return f"Document(doc_id={self.id}, content={self.content}, metadata={self.metadata})"                                                    
