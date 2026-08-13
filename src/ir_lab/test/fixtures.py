

class Fixtures:

    @staticmethod
    def query():
        from ir_lab.models.queries import Query
        return Query(
            id = 0,
            content = "information and retrieval"
        )

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

    

    @staticmethod
    def analyzed_documents():
        from ir_lab.models.documents import Document
        from ir_lab.models.documents import AnalyzedDocument
        from ir_lab.models.tokens import Token
        return [
                    AnalyzedDocument(
                        document=Document(
                            id=1,
                            content="information retrieval system information"
                        ),
                        tokens=[
                            Token("information", position=0),
                            Token("retrieval", position=1),
                            Token("system", position=2),
                            Token("information", position=3)
                        ],
                    ),
                    AnalyzedDocument(
                        document=Document(
                            id=2,
                            content="retrieval model"
                        ),
                        tokens=[
                            Token("retrieval", position=0),
                            Token("model", position=1),
                        ],
                    ),
                    AnalyzedDocument(
                        document=Document(
                            id=3,
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
    def rpn_stack() :
            from ir_lab.processing.boolean.boolean_rpn_parser import BooleanRPNParser

            parser = BooleanRPNParser()
            query = "information and retrieval"
            stack = parser(query)
            return stack
    
    @staticmethod
    def rpn_analyzed_stack() :
        from ir_lab.analyzing.analyzers import QueryAnalyzer
        stack = Fixtures.rpn_stack()
        analyzer = Fixtures.analyzer()
        q_analyzer = QueryAnalyzer(analyzer)
        q_analyzer(stack)
        return stack





    @staticmethod
    def analyzer_config():
        return {
            "character_filters" :[
                {
                    'type' : "ponctuation",
                    'replace' : " "
                }
            ],
            "tokenizer" : 
                {
                    "type" : "space"
                }
            ,
            "token_filters" : [
                {
                    "type" : "lowercase"
                }
            ]
        }


    @staticmethod 
    def analyzer():
        from ir_lab.analyzing.analyzers.analyzer_builder import AnalyzerBuilder
        config = Fixtures.analyzer_config()
        builder = AnalyzerBuilder()
        analyzer = builder.build(config)
        return analyzer

    @staticmethod
    def inverted_index() :
        from ir_lab.indexing.indexes import InvertedIndex
        index = InvertedIndex()

        index.add_posting(
            term="information",
            doc_id=0,
            positions=[1],
        )
        index.add_posting(
            term="information",
            doc_id=1,
            positions=[0, 3],
        )
        
        index.add_posting(
            term="information",
            doc_id=3,
            positions=[0],
        )

        index.add_posting(
            term="model",
            doc_id=2,
            positions=[1],
        )
        index.add_posting(
            term="model",
            doc_id=3,
            positions=[1],
        )

        index.add_posting(
            term="retrieval",
            doc_id=1,
            positions=[1],
        )
        index.add_posting(
            term="retrieval",
            doc_id=2,
            positions=[0],
        )
        index.add_posting(
            term="retrieval",
            doc_id=3,
            positions=[2],
        )

        index.add_posting(
            term="system",
            doc_id=1,
            positions=[2],
        )

        return index