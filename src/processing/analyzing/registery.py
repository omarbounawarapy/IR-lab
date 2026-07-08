import re


tokenizers ={
    "whitespace": lambda text: tokenize_whitespace(text),
    "regex": lambda **kwargs: lambda text: regex(text, **kwargs)
}
normalizers = {
    "lowercase": lambda text: lowercase(text),
    "remove_punctuation": lambda text: remove_punctuation(text)
}

def tokenize_whitespace(text):
    return text.split()
def regex(text, pattern=r'\w+'):
    return re.findall(pattern, text)
def lowercase(text):
    return text.lower()
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)