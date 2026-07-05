import re

tokenizers ={
    "whitespace": lambda **kwargs: whitespace,
    "regex": lambda **kwargs: lambda text: regex(text, **kwargs)
}
normalizers = {
    "lowercase": lambda **kwargs: lowercase,
    "remove_punctuation": lambda **kwargs: remove_punctuation}

def whitespace(text):
    return text.split()
def regex(text, pattern=r'\w+'):
    return re.findall(pattern, text)
def lowercase(text):
    return text.lower()
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)