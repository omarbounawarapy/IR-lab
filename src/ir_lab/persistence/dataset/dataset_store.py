from .dataset_registry import DatasetRegistery
from ir_lab.models.datasets import Dataset

class DatasetStore : 

    def __init__(self):
        pass 

    def load(dataset : str) -> Dataset : 
        loader = DatasetRegistery.get_loader(dataset) 
        return loader()


    
 
    