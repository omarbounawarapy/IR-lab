from .expirement import Expirement
from ir_lab.indexing.indexers.indexer_builder import IndexerBuilder
from ir_lab.analyzing.analyzers import AnalyzerBuilder, DocumentAnalyzer
from ir_lab.processing.processor_builder import ProcessorBuilder
from .run import Run


import hashlib
import json


class ExpirimentRunner:
    def __init__(self,dataset_store,index_store):
        self.dataset_store = dataset_store
        self.index_store = index_store
        self.indexer_builder = IndexerBuilder()
        self.analyzer_builder = AnalyzerBuilder()
        self.processor_builder = ProcessorBuilder()
        self.analyzers = {}

    def build(self,config : dict) -> Expirement :
        runs = []
        dataset = self.resolve_dataset(config["dataset"]["id"])

        for run_config in config["runs"] :
          analyzer_config = run_config["analysis"]
          index_config = run_config["index"]
          analyzer = self.resolve_analyzer(analyzer_config)
          index = self.resolve_index(index_config,analyzer_config,dataset)
          indexer = None if index is not None else self.indexer_builder(index_config)

          instance = Run(id = run_config['id'],
                         analyzer = analyzer,
                         processors=[],
                         config=run_config,
                         index=index,
                         indexer=indexer)
          runs.append(instance)

        return Expirement(
            dataset= dataset ,
            runs = runs
        )



    def resolve_dataset(self,dataset_id) :
      return self.dataset_store.load(dataset_id)





    def resolve_index(self,index_config,analyzer_config,dataset) :
            fingerprint = self.fingerprint_index(index_config,analyzer_config,dataset)

            if self.index_store.exist(fingerprint) :
                return self.index_store.load(fingerprint)
            return None

    @staticmethod
    def fingerprint_index(index_config,analyzer_config,dataset):
        dataset_id = dataset.id
        index_string = json.dumps(index_config, sort_keys=True, separators=(',', ':'))
        analyzer_string =  json.dumps(analyzer_config, sort_keys=True, separators=(',', ':'))
        data = index_string+analyzer_string+dataset_id
        return hashlib.sha256(data.encode('utf-8')).hexdigest()



    def resolve_analyzer(self,analyzer_config) :
        key = json.dumps(analyzer_config, sort_keys=True)
        if key not in self.analyzers:
            self.analyzers[key] = self.analyzer_builder(analyzer_config)
        return self.analyzers[key]

    def run(self,expirement : Expirement) :
        results = {}
        for run in expirement.runs:
            if run.index is None :
                document_analyzer = DocumentAnalyzer(run.analyzer)
                analyzed_docs = [document_analyzer(doc) for doc in expirement.dataset.corpus]
                run.index = run.indexer(analyzed_docs)
                fingerprint = self.fingerprint_index(
                    run.config["index"],
                    run.config["analysis"],
                    expirement.dataset,
                )
                self.index_store.save(run.index, fingerprint)

            processor = self.processor_builder(run.config["retrieval"], run.analyzer, run.index)
            run.processors = [processor]
            results[run.id] = processor(expirement.dataset.queries)

        return results


    def __call__(self,config : dict) :
        expirement = self.build(config)
        return self.run(expirement)
