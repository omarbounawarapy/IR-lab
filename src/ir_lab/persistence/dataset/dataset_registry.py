import json
from functools import wraps
from ir_lab.models.documents import Document
from ir_lab.models.queries import Query
from ir_lab.models.relevance import Qrel
from ir_lab.models.datasets import Dataset
from ir_lab.errors import DataError

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


def _load_json(path: str):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise DataError(f"dataset file not found: {path!r}")
    except json.JSONDecodeError as e:
        raise DataError(f"dataset file {path!r} is not valid JSON: {e}")


def _record(constructor, record, path):
    try:
        return constructor(record)
    except KeyError as e:
        raise DataError(f"{path!r} record is missing field {e}: {record!r}")


@DatasetRegistry.register("toy")
def toy_loader():
    path = "datasets/toy/dataset.json"
    dataset = _load_json(path)

    docs = [
        _record(
            lambda d: Document(
                id=d["doc_id"],
                content=d["text"],
                metadata={"title": d["title"]},
            ),
            doc,
            path,
        )
        for doc in dataset["documents"]
    ]
    queries = [
        _record(
            lambda q: Query(id=q["query_id"], content=q["text"]),
            q,
            path,
        )
        for q in dataset["queries"]
    ]
    qrels = [
        _record(
            lambda qr: Qrel(
                query_id=qr["query_id"],
                document_id=qr["doc_id"],
                metadata={"relevance": qr["relevance"]},
            ),
            qr,
            path,
        )
        for qr in dataset["qrels"]
    ]

    return Dataset(
        id="toy",
        corpus=docs,
        querries=queries,
        qrels=qrels,
    )


@DatasetRegistry.register("cisi")
def cisi_loader():
    docs_path = "datasets/cisi/documents.json"
    queries_path = "datasets/cisi/queries.json"
    qrels_path = "datasets/cisi/qrels.json"

    docs = [
        _record(
            lambda d: Document(
                id=d["id"],
                content=d["text"],
                metadata={
                    "title": d["title"],
                    "authors": d["authors"],
                    "references": d["references"],
                },
            ),
            doc,
            docs_path,
        )
        for doc in _load_json(docs_path)
    ]

    queries = [
        _record(
            lambda q: Query(id=q["id"], content=q["text"]),
            q,
            queries_path,
        )
        for q in _load_json(queries_path)
    ]

    qrels = [
        _record(
            lambda qr: Qrel(query_id=qr["query_id"], document_id=qr["document_id"]),
            qr,
            qrels_path,
        )
        for qr in _load_json(qrels_path)
    ]

    return Dataset(
        id="cisi",
        corpus=docs,
        querries=queries,
        qrels=qrels,
    )
