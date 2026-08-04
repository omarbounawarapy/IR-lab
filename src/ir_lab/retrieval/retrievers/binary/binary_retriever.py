from ir_lab.indexing.indexes import InvertedIndex
class BinaryRetriever:
    def __init__(self, index: InvertedIndex):
        self.index = index
        """
        self.querry_parsers={
            BooleanASTQuery: BooleanASTParser(),
            BooleanRPNQuery: BooleanRPNParser()
        }
        """

    """
    find the intersection list of two doc_id list
    """
    def intersect(self,docs1,docs2):
        return docs1 & docs2
    def union(self,docs1,docs2):
        return docs1 | docs2
    
    """
    def retrieve(self, query: ExecutableQuerry ) -> set:
        parser = self.querry_parsers.get(type(query))
        if parser is None:
            raise ValueError(f"No parser found for query type: {type(query)}")
        return parser(query)
        
    
    def booleanRPNEvaluator(self, query: BooleanRPNQuery) -> list[Document]:
        data = query.data 
        cache = {}
        solve_stack=[]
        for argument in data : 
            if argument in ("AND","OR","NOT"):
                pass 
            else : 
                posting_list = self.index.querry(argument)
                cache[argument] = posting_list
    """         


if __name__ == "__main__" : 
    from ir_lab.test import Fixtures
    index = Fixtures.inverted_index()
    retriver = BinaryRetriever(index)
    docs1 = index.get_term_documents("information")
    docs2 = index.get_term_documents("model")

    print(f"{retriver.intersect(docs1,docs2)=}")
    print(f"{retriver.union(docs1,docs2)=}")

    