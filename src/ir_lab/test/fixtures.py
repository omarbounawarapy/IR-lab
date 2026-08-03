
from ir_lab.models import documents,tokens

class Fixtures:

    @staticmethod
    def document():
        return documents.Document(
            id="doc1",
            text="Hello, WORLD! This is a test-document. NLP's preprocessing isn't easy: version 2.0."
        )

    @staticmethod
    def token():
        return tokens.Token(
            content= "UPPER lower.12347896 ./§§§%"
        )

    @staticmethod
    def text():
        return "Hello, WORLD! This is a test-document. NLP's preprocessing isn't easy: version 2.0."
        

