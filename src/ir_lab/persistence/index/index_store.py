
class IndexStore : 
    def __init__(self):
        self.registery = {

        }


    def exist(self,md5 ) : 
        return md5 in self.registery

    def load(self,md5):
        return self.registery[md5]
    def save(self,index,md5):
        self.registery[md5] = index

