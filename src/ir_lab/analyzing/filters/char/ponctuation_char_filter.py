import string
from .char_filter import CharFilter




class PonctuationCharFilter(CharFilter):
    def __init__(self,replace:None):
        self.replace = replace

    def apply(self,text:str)->str : 
        punctuation_map = str.maketrans({char: self.replace for char in string.punctuation})
        result = text.translate(punctuation_map)
        return result


if __name__ == "__main__" : 
    from ir_lab.test import Fixtures
    text = Fixtures.text()
    cls = PonctuationCharFilter(" ")
    print(f"{cls(text)=}")


