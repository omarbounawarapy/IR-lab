from .analysis_result import AnalysisResult

class Analyzer:
    def __init__(self,config):

        self.character_filters = config["character_filters"]
        self.tokenizer = config["tokenizer"]
        self.token_filters= config["token_filters"]

        

    def analyze_content(self, text : str) -> AnalysisResult: 

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


