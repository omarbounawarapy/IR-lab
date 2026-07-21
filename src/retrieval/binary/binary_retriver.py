class BinaryRetriever:
    def __init__(self, index: InvertedIndex):
        self.index = index
        self.querry_parsers={
            BooleanASTQuery: BooleanASTParser(),
            BooleanRPNQuery: BooleanRPNParser()
        }
    

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
                

