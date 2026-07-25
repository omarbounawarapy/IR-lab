from .analysis_result import AnalysisResult

class Analyzer:
    def __init__(self, steps):
        self.character_filters = steps.get("character_filters",[])
        self.tokenizer = steps.get("tokenizer",[])
        self.token_filters= steps.get("token_filters",[])

        

    def analyze(self, text : str) -> AnalysisResult: 

        for filter in self.character_filters:
            text = filter.apply(text)

        tokens = self.tokenizer.tokenize(text)

        for filter in self.token_filters:
            tokens = filter.apply(tokens)

        results = AnalysisResult(tokens)
        return results