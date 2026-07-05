class ToyReader:
    def read(self, file_path):
        """
        Reads a toy dataset from the specified file path.

        Args:
            file_path (str): The path to the toy dataset file.
        """
        with open(file_path, 'r') as file:
            text = file.read()
            return text