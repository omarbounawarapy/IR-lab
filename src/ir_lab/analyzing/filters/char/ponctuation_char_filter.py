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
    text = "omar.bounawara.py@gmail.com"
    cls = PonctuationCharFilter(" ")
    text = cls(text)
    print(text)


