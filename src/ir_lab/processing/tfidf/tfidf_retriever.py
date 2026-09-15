import math

from ir_lab.indexing.indexes import InvertedIndex


class TFIDFRetriever:
    """Ranked vector-space retrieval over the same InvertedIndex boolean
    retrieval uses -- Posting.tf and TermInfo.document_frequency were
    always collected (Section 1.4 of the assessment), this is the first
    thing to actually consume them."""

    def __init__(self, index: InvertedIndex):
        self.index = index

    def idf(self, term: str) -> float:
        df = len(self.index.get_postings(term))
        if df == 0:
            return 0.0
        return math.log(self.index.n_doc / df)

    def score(self, terms: list[str]) -> list[tuple]:
        """Returns (doc_id, score) pairs, ranked descending by score,
        ties broken by doc_id for a deterministic order."""
        scores: dict = {}
        for term in terms:
            postings = self.index.get_postings(term)
            if not postings:
                continue
            idf = math.log(self.index.n_doc / len(postings))
            for posting in postings:
                scores[posting.doc_id] = scores.get(posting.doc_id, 0.0) + posting.tf * idf

        return sorted(scores.items(), key=lambda item: (-item[1], item[0]))
