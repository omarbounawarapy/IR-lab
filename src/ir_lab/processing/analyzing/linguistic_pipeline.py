from registery import *
from models.documents import Document,AnalyzedDocument

"""
Linguistic Pipeline for processing text through various tokenization and normalization steps.
"""





class Linguistic_Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def process(self, document : Document) -> AnalyzedDocument:
        for (step, meta) in self.steps:
            step_cls = normalizers.get(step) or tokenizers.get(step)
            content = getattr(document,"content","")
            tokens = step_cls(**meta)(content)
            analyzed_document = AnalyzedDocument(document,tokens)
        return analyzed_document


if __name__ == "__main__" : 
    p = Linguistic_Pipeline(
        ("lowercase",()),
        ("whitespace",()),
    )
    d = Document(
        doc_id="test_doc",
        content="apple pie is delicious",
    )
    ad = p.process(d) 
    print(ad)