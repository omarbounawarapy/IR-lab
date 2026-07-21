class Query:
    def __init__(self, query_id: str, text: str, metadata: dict = None):
        self.query_id = query_id
        self.text = text
        self.metadata = metadata if metadata is not None else {}

    def __repr__(self):
        return f"Query(query_id={self.query_id}, text={self.text}, metadata={self.metadata})"