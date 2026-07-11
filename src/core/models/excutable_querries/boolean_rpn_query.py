"""
builds an rpn excutable query 
"""


from .executable_query import ExecutableQuery


class BooleanRPNQuery(ExecutableQuery):
    def __init__(self, data:any):
        self.data = data

    


    
