from .analysis_result import AnalysisResult
from ir_lab.core import ComponentBuilder

class Analyzer:
    def __init__(self,
                 charachter_filters,
                 tokenizer,
                 token_filters):
        self.character_filters = charachter_filters
        self.tokenizer = tokenizer
        self.token_filters= token_filters

        

    def analyze(self, text : str) -> AnalysisResult: 

        for filter in self.character_filters:
            text = filter(text)

        tokens = self.tokenizer(text)

        analyzed=[]
        for token in tokens:
          for step in self.token_filters:
            token = step(token)
            if token is None:
                 break
             
          if token is not None:
             analyzed.append(token)


        results = AnalysisResult(analyzed)
        return results


if __name__ == '__main__' : 
    from ir_lab.test import Fixtures
    text =  Fixtures.text()