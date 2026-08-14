
from json import loads

class expirement : 
    def __init__(self,file_path):
        self.config = loads(open(file_path, "r"))


    def  load_config(self,config) : 
        self.runs = {
            
        }