from information_retrival_lab.src.core.models.document import Document
class ToyAdapter:
    def __init__(file_path:str):
        self.file_path = file_path
        self.current_doc_id = 0

    def adapt(self, text:str):
        """
        Adapts the toy dataset text into a list of Document objects.

        Args:
            text (str): The raw text from the toy dataset.

        Returns:
            a document Object containing the content and metadata.
        """
        
        doc = Document(doc_id=self.current_doc_id, content=text, metadata={"source": self.file_path})
        self.current_doc_id += 1
        return doc

