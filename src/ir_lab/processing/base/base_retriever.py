
from abc import ABC

from ir_lab.indexing.indexes import BaseIndex

class BaseRetriver(ABC):
    def __init__(self, index: BaseIndex):
        self.index = index


  