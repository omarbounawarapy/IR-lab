from functools import wraps 
from json import load
from ir_lab.models.documents import Document
from ir_lab.models.queries import Query
from ir_lab.models.relevance import Qrel
from ir_lab.models.datasets import Dataset

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


@DatasetRegistry.register("toy")
def toy_loader():
    dataset = load(open("datasets/toy/dataset.json"))
    docs=  [ Document(
            id = doc["doc_id"],
            content = doc["text"],
            metadata = {
                "title" : doc["title"],
            }
            
        )
        for doc in dataset['documents']
    ]
    queries = [
        Query(
            id = q["query_id"],
            content = q["text"]
        )
        for q in dataset["queries"]
    ]
    qrels = [
        Qrel(
            query_id = qr["query_id"],
            document_id=qr["doc_id"],
            metadata={
                "relevance" : qr["relevance"]
            }

        )
        for qr in dataset['qrels']
    ]

    return Dataset(
        corpus=docs, 
        queries= queries,
        qrels= qrels
    )


@DatasetRegistry.register("cisi")
def cisi_loader():
    docs_path = "datasets/cisi/documents.json"
    queries_path = "datasets/cisi/queries.json"
    qrels_path = "datasets/cisi/qrels.json"
    
    qrels =  load(open(docs_path,"r"))
    docs = [
        Document(
            id = doc["id"],
            content = doc["text"],
            metadata = {
                "title" : doc["title"],
                "authors" : doc["authors"],
                "references" : doc["references"]
            }
        )
        for doc in load(open(docs_path,"r"))
    ]

    queries = [
        Query(
            id =  q["id"],
            content = q["text"],
        )
        for q in load(open(queries_path))
    ]

    qrels = [
            Qrel(
                query_id =  qr["query_id"],
                document_id= qr["document_id"]
            )
            for qr in load(open(qrels_path))
    ]

    return Dataset(
        id = "cisi",
        corpus= docs,
        queries = queries,
        qrels = qrels
    )


