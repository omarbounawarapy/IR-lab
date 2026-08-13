from ir_lab.models.documents import AnalyzedDocument
from .analyzer import Analyzer

class DocumentAnalyzer:

    def __init__(self, analyzer : Analyzer ) :
        self.analyzer = analyzer

    def analyze(self, document)-> AnalyzedDocument:
        analysis_results = self.analyzer.analyze_content(document.content)
        tokens = getattr(analysis_results,"tokens",[])

        return AnalyzedDocument(
            document=document,
            tokens=tokens,
        )



if __name__ == "__main__" : 
    from ir_lab.test import Fixtures
    document = Fixtures.document()
    analyzer = Fixtures.analyzer()
    
    doc_analyzer = DocumentAnalyzer(analyzer=analyzer)
    analyzed_doc = doc_analyzer.analyze(document)
    for token in analyzed_doc.tokens:
        print(f"{token=}")

    