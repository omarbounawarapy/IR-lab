
from dataclasses import dataclass
from ir_lab.indexing.indexes import BaseIndex
from ir_lab.indexing.indexers.base_indexer import BaseIndexer
from ir_lab.analyzing.analyzers.analyzer import Analyzer
from typing import Any

@dataclass
class Run:
    id: str
    analyzer: Analyzer
    processors: list[Any]
    config: dict
    index: BaseIndex | None = None
    indexer: BaseIndexer | None = None