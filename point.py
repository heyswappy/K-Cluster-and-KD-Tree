class point:
    "K-D POINT CLASS"
    def __init__(self,coordinate, name=None, dim=None):
        """ name, dimension and coordinates """
        self.name = name
        if type(dim) == type(None):
            self.dim = len(coordinate)
        else:
            self.dim = dim
        if len(coordinate) == self.dim:
            self.coordinate = coordinate
        else:
            raise Exception("INVALID DIMENSIONAL INFORMATION WHILE CREATING A POINT")

    def getx(self):
        if self.dim >= 1:
            return self.coordinate[0]
        else:
            return None

    def gety(self):
        if self.dim >= 2:
            return self.coordinate[1]
        else:
            return None

    def getz(self):
        if self.dim >= 3:
            return self.coordinate[2]
        else:
            return None

    def get(self,k):
        if self.dim >= k:
            return self.coordinate[k]
        else:
            return None

    def print(self):
        print("Name:",self.name,"Dim:",self.dim,"Coordinates:",self.coordinate)
        return

    def __eq__(self, other):
        if (type(self) != type(None) and type(other) == type(None)) or (type(self) == type(None) and type(other) != type(None)):
            return False
        if self.dim == other.dim and self.coordinate == other.coordinate:
            return True
        return False

    def __ne__(self, other):
        if (type(self) != type(None) and type(other) == type(None)) or (type(self) == type(None) and type(other) != type(None)):
            return False
        if self.dim != other.dim or self.coordinate != other.coordinate:
            return True
        return False

    def __lt__(self, other):
        '''overload lesser than operator mainly for heapq'''
        t = self.coordinate < other.coordinate
        return t

    def __gt__(self, other):
        '''overload greater than operator mainly for heapq'''
        t = self.coordinate > other.coordinate
        return t

    def copy(self):
        k = point(self.coordinate, self.name, self.dim)
        return k

    def distance(self, other):
        if self.dim != other.dim:
            return None
        dist = 0
        for i in range(self.dim):
            dist += (self.coordinate[i] - other.coordinate[i])**2
        dist = dist**0.5
        return dist

    def in_range(self, bounds):
        """return true if a point lies within given bounds"""
        if len(bounds) != self.dim:
            raise Exception("DIMENSIONAL INCONSISTENCY WHILE CALLING IN_RANGE")
        for i in range(self.dim):
            if(not(bounds[i][0] <= self.coordinate[i] <= bounds[i][1])):
                return False
        return True