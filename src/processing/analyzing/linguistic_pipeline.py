from .registery import tokenizers, normalizers

"""
Linguistic Pipeline for processing text through various tokenization and normalization steps.
"""





class Linguistic_Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def process(self, text):
        for (step, meta) in self.steps:
            step_cls = normalizers.get(step) or tokenizers.get(step)
            text = step_cls(**meta)(text)
        return text