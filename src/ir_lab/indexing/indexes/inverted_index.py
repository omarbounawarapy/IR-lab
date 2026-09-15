from .base_index import BaseIndex
from dataclasses import dataclass

@dataclass
class Posting:
    doc_id: int
    tf: int
    positions: list[int]

@dataclass
class TermInfo:
    term: str
    corpus_tf: int
    document_frequency: int
    idf: float | None = None



class InvertedIndex(BaseIndex):
    def __init__(self):
        super().__init__()
        self.vocabulary: dict[str, int] = {}
        self.postings: dict[str, list[Posting]] = {}
        self.term_info: dict[int, TermInfo] = {}
        self.doc_ids: set = set()

    @property
    def n_doc(self) -> int:
        return len(self.doc_ids)

    def document_ids(self) -> list:
        return sorted(self.doc_ids)

    def get_postings(self,term):
        if term not in self.vocabulary:return []
        else :
            return self.postings[term]

    def get_term_documents(self, term) -> list:

        return [posting.doc_id for posting in self.get_postings(term)]


    def add_posting(self,term,doc_id,positions):
        self.doc_ids.add(doc_id)
        if not super().in_vocabulary(term):

            self.vocabulary[term] = len(self.vocabulary)
            self.postings[term] = []
            self.term_info[self.vocabulary[term]]= TermInfo(
                term = term,
                corpus_tf=0,
                document_frequency=0
                )
        posting = Posting(
            doc_id = doc_id,
            tf = len(positions),
            positions = positions
            )
        self.postings[term].append(posting)
        info = self.term_info[self.term_id(term)]
        info.corpus_tf+=len(positions)
        info.document_frequency+=1


    def term_id(self,term):
        return self.vocabulary[term]

    def __repr__(self):
        return (
            f"INVERTED INDEX("
            f"vocabulary={self.vocabulary!r}, "
            f"LISTS={self.postings!r}"
            f")"
        )
