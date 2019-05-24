from point import point
class node:
    "GRAPH NODE CLASS"
    def __init__(self, key, coordinate, cost=None):
        self.key = key
        self.nbr = {} # key is key and value would be reference to node type object
        self.wt = {} # hashtable to store extra value particular to two nodes
        self.point = point(coordinate, key)
        self.land_cost = cost
        return
    
    def addNbr(self, key, nodeRef, wt = None):
        if key == self.key:
            return
        if key not in self.nbr:
            self.nbr[key] = nodeRef
            self.wt[key] = wt
        return