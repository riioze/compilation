from parser import *

class Optimizer:
    def __init__(self,parser:Parser):
        self.parser = parser
    
    def next_tree(self):
        return self.parser.next_tree()