from functools import wraps 
from json import load



class DatasetRegistry:

    loaders = {}

    @classmethod
    def register(cls, dataset):
        def decorator(func):
            @wraps(func)
            def wrapper():
                return func()

            cls.loaders[dataset] = wrapper
            return wrapper

        return decorator

    @classmethod
    def load(cls, dataset):
        return cls.loaders[dataset]()

    @classmethod
    def get_loader(cls,dataset : str) -> callable : 
        return cls.loaders.get(dataset)

    


@DatasetRegistry.register("cisi")
def cisi_loader():
    docs_path = "datasets/cisi/documents.json"
    queries_path = "datasets/cisi/queries.json"
    qrels_path = "datasets/cisi/qrels.json"
    docs =  load(open(docs_path,"r"))
    queries = load(open(docs_path,"r"))
    qrels =  load(open(docs_path,"r"))
    print(docs[0])

if __name__ == "__main__":
    cisi_loader()