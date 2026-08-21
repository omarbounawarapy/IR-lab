from .expirement import Expirement
from ir_lab.indexing.indexers.indexer_builder import IndexerBuilder
from ir_lab.analyzing.analyzers import Analyzer , AnalyzerBuilder
from ir_lab.indexing.indexes import BaseIndex
from .run import Run

class ExpirimentRunner:
    def __init__(self,dataset_store,index_store):
        self.dataset_store = dataset_store
        self.index_store = index_store
        self.indexer_builder = IndexerBuilder()
        self.analyzer_builder = AnalyzerBuilder()
        self.analyzers = {}

    def build(self,config : dict) -> Expirement :
        runs = []
        dataset = self.resolve_dataset(config["dataset"])
        
        
        for run in config["runs"] : 
          analyzer = self.resolve_analyzer(run["analyzing"]) 
          index = self.resolve_index(run["index"],dataset)
          runs.append(Run(
              id = run["id"],
              index = index,
              analyzer= analyzer
          ))

        return Expirement(
            dataset= dataset ,
            runs = runs
        )



    def resolve_dataset(self,dataset) : 
      return self.dataset_store.load(dataset)
    



         
    def resolve_index(self,index_config,dataset) -> BaseIndex : 
            if self.index_store.exist(index_config , dataset.id) : 
                index = self.index_store.load(index_config)
            else : 
                indexer = self.indexer_builder(index_config)
                index = indexer(index)
            return index



    def resolve_analyzer(self,run) -> Analyzer: 
        analyzer_config =  run["analyzing"]
        analyzer_hash = hash(analyzer_config)
        if analyzer_hash in self.analyzers:
            analyzer = self.analyzers[analyzer_hash]
        else : 
            analyzer = self.analyzer_builder(analyzer_config)
            self.analyzers[analyzer_hash] = analyzer
        return analyzer

    def run(self,expirement : Expirement)   : 
        pass

    


    def __call__(self,config : dict) : 
        expirement = self.build(config)
        self.run(expirement)