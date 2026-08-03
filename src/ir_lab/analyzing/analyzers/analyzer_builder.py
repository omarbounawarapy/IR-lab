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

    def build(self,config):
        character_filters = ComponentBuilder.build(
            config["character_filters"],
            CHARACTER_FILTERS,
        )

        tokenizer = ComponentBuilder.build(
            [config["tokenizer"]],
            TOKENIZERS,
        )[0]

        token_filters = ComponentBuilder.build(
            config["token_filters"],
            TOKEN_FILTERS,
        )

        return Analyzer(
            character_filters,
            tokenizer,
            token_filters,
        )