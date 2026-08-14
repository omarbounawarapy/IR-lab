from dataclasses import dataclass
from ir_lab.models.queries import Query
from ir_lab.models.documents import Document
from ir_lab.models.relevance import Qrel



@dataclass
class Dataset:
    def __init__(self,id : str , corpus:list[Document] , querries : list[Query],qrels : list[Qrel],meta:dict):
        self.id = id 
        self.corpus = corpus
        self.queries = querries
        self.qrels = qrels
        self.meta = meta

