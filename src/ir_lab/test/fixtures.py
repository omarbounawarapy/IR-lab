
from ir_lab.models import documents

class Fixtures:

    @staticmethod
    def document():
        return documents.Document(
            id="doc1",
            text="information retrieval is..."
        )

