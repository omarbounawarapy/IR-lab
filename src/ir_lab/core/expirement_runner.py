from .expirement import Expirement
from ir_lab.indexing.indexers.indexer_builder import IndexerBuilder
from ir_lab.analyzing.analyzers import AnalyzerBuilder, DocumentAnalyzer
from ir_lab.processing.processor_builder import ProcessorBuilder
from ir_lab.evaluation.metrics import evaluate_run
from ir_lab.errors import ConfigError
from ir_lab.reproducibility import set_global_seed, DEFAULT_SEED
from .run import Run
from .run_record import build_run_record


import hashlib
import json


def _required(config, key, where):
    try:
        return config[key]
    except KeyError:
        raise ConfigError(f"{where} is missing required field {key!r}: {config!r}")


class ExpirimentRunner:
    def __init__(self,dataset_store,index_store,run_store=None):
        self.dataset_store = dataset_store
        self.index_store = index_store
        self.run_store = run_store
        self.indexer_builder = IndexerBuilder()
        self.analyzer_builder = AnalyzerBuilder()
        self.processor_builder = ProcessorBuilder()
        self.analyzers = {}

    def build(self,config : dict) -> Expirement :
        runs = []
        dataset_config = _required(config, "dataset", "experiment config")
        dataset_id = _required(dataset_config, "id", "experiment config 'dataset'")
        dataset = self.resolve_dataset(dataset_id)

        for run_config in _required(config, "runs", "experiment config") :
          run_id = _required(run_config, "id", "run config")
          analyzer_config = _required(run_config, "analysis", f"run {run_id!r} config")
          index_config = _required(run_config, "index", f"run {run_id!r} config")
          _required(run_config, "retrieval", f"run {run_id!r} config")
          analyzer = self.resolve_analyzer(analyzer_config)
          index = self.resolve_index(index_config,analyzer_config,dataset)
          indexer = None if index is not None else self.indexer_builder(index_config)

          instance = Run(id = run_id,
                         analyzer = analyzer,
                         processors=[],
                         config=run_config,
                         index=index,
                         indexer=indexer)
          runs.append(instance)

        meta = config.get("meta", {})
        return Expirement(
            dataset= dataset ,
            runs = runs,
            id = meta.get("id"),
            seed = config.get("seed"),
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
        set_global_seed(expirement.seed if expirement.seed is not None else DEFAULT_SEED)

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
            run_results = processor(expirement.dataset.queries)
            results[run.id] = run_results

            if self.run_store is not None:
                evaluation = None
                if expirement.dataset.qrels:
                    evaluation = evaluate_run(expirement.dataset.queries, run_results, expirement.dataset.qrels)

                record = build_run_record(
                    experiment_id=expirement.id,
                    run_config_id=run.id,
                    run_config=run.config,
                    dataset_id=expirement.dataset.id,
                    queries=expirement.dataset.queries,
                    run_results=run_results,
                    seed=expirement.seed,
                    evaluation=evaluation,
                )
                self.run_store.save(record)

        return results


    def __call__(self,config : dict) :
        expirement = self.build(config)
        return self.run(expirement)
