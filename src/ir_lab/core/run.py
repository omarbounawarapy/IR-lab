
from dataclasses import dataclass
from typing import Any

from ir_lab.analyzing.analyzers.analyzer import Analyzer
from ir_lab.indexing.indexers.base_indexer import BaseIndexer
from ir_lab.indexing.indexes import BaseIndex


@dataclass
class Run:
    id: str
    analyzer: Analyzer
    processors: list[Any]
    config: dict
    index: BaseIndex | None = None
    indexer: BaseIndexer | None = None