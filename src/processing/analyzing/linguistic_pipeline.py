from .registery import tokenizers, normalizers
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