from .analyzer import Analyzer

from ir_lab.analyzing.filters.token import LowerCaseTokenFilter
from ir_lab.analyzing.filters.char import PonctuationCharFilter
from ir_lab.analyzing.tokenizers import SpaceTokenizer

from ir_lab.core import ComponentBuilder

CHARACTER_FILTERS = {
    "ponctuation" : PonctuationCharFilter

}
TOKEN_FILTERS = {
    "lowercase" : LowerCaseTokenFilter

}

TOKENIZERS= {
    "space" : SpaceTokenizer

}


class AnalyzerBuilder():

    def __init__(self):
        pass 

    def build(self,config) -> Analyzer:
        character_filters = ComponentBuilder.build(
            config["character_filters"],
            CHARACTER_FILTERS,
        )
    
        tokenizer = ComponentBuilder.build(
            [config["tokenizer"][0]],
            TOKENIZERS
        )[0]

        token_filters = ComponentBuilder.build(
            config["token_filters"],
            TOKEN_FILTERS,
        )
        config = {
            "token_filters" : token_filters,
            "tokenizer" : tokenizer,
            "character_filters" : character_filters
        }

        return Analyzer(config)
    def __call__(self,config):
        self.build(config)