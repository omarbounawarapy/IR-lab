class Query:
    def __init__(self, id: int, content: str, metadata: dict = None):
        self.id = id
        self.content = content
        self.metadata = metadata if metadata is not None else {}

    def __repr__(self):
        return f"Query(query_id={self.id}, text={self.text}, metadata={self.metadata})"