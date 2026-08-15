from ir_lab.indexing.indexes import InvertedIndex
from ir_lab.models.tokens import Token
class BooleanRetriever:
    def __init__(self, index: InvertedIndex):
        self.index = index

    def intersect(self,docs1,docs2):
        
        if isinstance(docs1,list) :
            docs1 =  docs1[0]
            docs1 = self.index.get_term_documents(docs1.content)
        if isinstance(docs2,list) :
            docs2 =  docs2[0]
            docs2 = self.index.get_term_documents(docs2.content)


        i,j=0,0
        results=[]
        while i<len(docs1) and j<len(docs2):
            if docs1[i]>docs2[j]:
                j+=1
            elif docs1[i]< docs2[j]:
                i+=1
            else :
                results.append(docs1[i])
                i+=1
                j+=1
        return results

    
    def union(self, docs1, docs2):
        i = j = 0
        result = []

        while i < len(docs1) and j < len(docs2):
            if docs1[i] < docs2[j]:
                result.append(docs1[i])
                i += 1
            elif docs1[i] > docs2[j]:
                result.append(docs2[j])
                j += 1
            else:
                result.append(docs1[i])
                i += 1
                j += 1

        result.extend(docs1[i:])
        result.extend(docs2[j:])

        return result
    
    def complement(self,docs1):
        i,j=0,0
        results=[]
        docs2 = [i for i in range(self.index.n_doc+1)]
        while i<len(docs1) and j<len(docs2):
            if docs1[i]>docs2[j]:
                results.append(docs2[j])
                j+=1
            elif docs1[i]< docs2[j]:
                i+=1
            else :
                i+=1
                j+=1
        results.extend(docs2[j:])
        
        return results
    
    def and_not(self,docs1,docs2):
        i,j=0,0
        results=[]
        while i<len(docs1) and j<len(docs2):
            if docs1[i]>docs2[j]:
                j+=1
            elif docs1[i]< docs2[j]:
                results.append(docs1[i])
                i+=1
            else :
                i+=1
                j+=1
        results.extend(docs1[i:])
        
        return results

    



if __name__ == "__main__" : 
    from ir_lab.test import Fixtures
    index = Fixtures.inverted_index()
    retriver = BinaryRetriever(index)
    docs1 = index.get_term_documents("information")
    docs2 = index.get_term_documents("model")
    print(f"{retriver.index=}")
    
    print(f"{retriver.intersect(docs1,docs2)=}")
    print(f"{retriver.union(docs1,docs2)=}")
    print(f"{retriver.complement(docs1)=}")
    print(f"{retriver.and_not(docs1,docs2)=}")


    