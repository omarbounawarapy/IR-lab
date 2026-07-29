

class Fixtures:

    @staticmethod
    def document():
        from ir_lab.models import documents
        return documents.Document(
            id="doc1",
            content="Hello, WORLD! This is a test-document. NLP's preprocessing isn't easy: version 2.0."
        )

    @staticmethod
    def token():
        from ir_lab.models import tokens

        return tokens.Token(
            content= "UPPER lower.12347896 ./§%"
        )

    @staticmethod
    def text():
        return "Hello, WORLD! This is a test-document. NLP's preprocessing isn't easy: version 2.0."

    

    def analyzed_documents():
        from ir_lab.models.documents import Document
        from ir_lab.models.documents import AnalyzedDocument
        from ir_lab.models.tokens import Token
        return [
                    AnalyzedDocument(
                        document=Document(
                            id="D1",
                            content="information retrieval system"
                        ),
                        tokens=[
                            Token("information", position=0),
                            Token("retrieval", position=1),
                            Token("system", position=2),
                        ],
                    ),
                    AnalyzedDocument(
                        document=Document(
                            id="D2",
                            content="retrieval model"
                        ),
                        tokens=[
                            Token("retrieval", position=0),
                            Token("model", position=1),
                        ],
                    ),
                    AnalyzedDocument(
                        document=Document(
                            id="D3",
                            content="information model retrieval"
                        ),
                        tokens=[
                            Token("information", position=0),
                            Token("model", position=1),
                            Token("retrieval", position=2),
                        ],
                    ),
                ]

    






    @staticmethod
    def analyzer_config():
        return {
            "character_filters" :[
                {
                    'type' : "ponctuation",
                    'replace' : " "
                }
            ],
            "tokenizer" : [
                {
                    "type" : "space"
                }
            ],
            "token_filters" : [
                {
                    "type" : "lowercase"
                }
            ]
        }