class kd_node:
    "K DIMENSIONAL TREE NODE"
    def __init__(self, split_over=None, dim=None, left=None, right=None, parent=None):
        self.split_over = split_over
        self.dim = dim
        self.L = left
        self.R = right
        self.P = parent

    def copy(self):
    	t = kd_node(split_over=self.split_over, dim=self.dim)
    	return t
    def print(self):
        print("SPLITTING OVER VALUE", self.split_over, "ON DIMENSION", self.dim)