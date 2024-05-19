class Ques_1:

    def __init__(self):
        self.node = []
    
    def add(self, node):
        self.node.insert(0, node)
        #return self.node

    def rem(self):
        a = self.node.pop()
        return a

    def size(self):
        return len(self.node)
    
    def is_empty(self):
        self.node.clear()