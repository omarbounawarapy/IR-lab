
from dataclasses import dataclass
from ir_lab.indexing.indexes import BaseIndex
from ir_lab.analyzing.analyzers import Analyzer



@dataclass 
class Run : 
    id : str 
    index : BaseIndex 
    analyzer : Analyzer
    
