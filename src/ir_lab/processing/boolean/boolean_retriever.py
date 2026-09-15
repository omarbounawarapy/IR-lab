from ir_lab.indexing.indexes import InvertedIndex


class BooleanRetriever:
    def __init__(self, index: InvertedIndex):
        self.index = index

    def term_documents(self, term: str):
        return self.index.get_term_documents(term)

    def intersect(self,docs1,docs2):
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
        excluded = set(docs1)
        return [doc_id for doc_id in self.index.document_ids() if doc_id not in excluded]

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
    retriver = BooleanRetriever(index)
    docs1 = index.get_term_documents("information")
    docs2 = index.get_term_documents("model")
    print(f"{retriver.index=}")

    print(f"{retriver.intersect(docs1,docs2)=}")
    print(f"{retriver.union(docs1,docs2)=}")
    print(f"{retriver.complement(docs1)=}")
    print(f"{retriver.and_not(docs1,docs2)=}")
