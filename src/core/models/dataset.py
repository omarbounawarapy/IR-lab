from information_retrival_lab.src.io import adapters,parsers,readers




class Dataset:
    def __init__(self,path: str,metadata: dict = None):
        self.folder_path = path
        self.documents = []
        self.metadata = metadata or {}
        self.adapter = adapters[metadata.get("adapter", "toy_adapter")]()
        self.reader = readers[metadata.get("reader", "toy_reader")]()
        self.parser = parsers[metadata.get("parser", "toy_parser")]() 

    def load(self):
        """
        Loads the dataset by reading, parsing, and adapting the data.

        Returns:
            list: A list of Document objects.
        """
        text = self.reader.read(self.folder_path)
        parsed_data = self.parser.parse(text)
        for item in parsed_data:
            doc = self.adapter.adapt(item)
            self.documents.append(doc)
        return self.documents