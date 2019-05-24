from point import point
from kd_node import kd_node
import heapq
class kd_tree:
    "K DIMENSIONAL TREE"
    def __init__(self, dim):
        self.head = None
        self.dim = dim
        self.count = 0

    def build(self, point_data):
        """the dim arguemnt tells which dimesnsion the split happened on previously so change it accordingly first;
        on and self.dim is the total number of dimensions"""
        self.count = len(point_data)
        dim = 0
        new_dim = (dim+1)%self.dim
        L, R, T= self.split(point_data, dim)
        new_node = kd_node(split_over = T, dim = dim)
        new_node.L = self._buildRec(L, new_dim, new_node)
        new_node.R = self._buildRec(R, new_dim, new_node)
        self.head = new_node;
        return
    
    def _buildRec(self, point_data, dim, parent):
        """the dim arguemnt tells which dimesnsion the split happened on previously so change it accordingly first;
        on and self.dim is the total number of dimensions"""
        if point_data == None:
            return None
        l = len(point_data)
        if l==0:
            return None
        if l==1:
            return point_data[0]
        """above are the terminating conditions"""
        new_dim = (dim+1)%self.dim
        L, R, T = self.split(point_data, dim)
        new_node = kd_node(split_over = T, dim = dim, parent = parent)
        new_node.L = self._buildRec(L, new_dim, new_node)
        new_node.R = self._buildRec(R, new_dim, new_node)
        return new_node;

    def split(self, point_data, dim):
        avg = 0
        for i in point_data:
            avg += i.get(dim)
        avg = avg/(len(point_data))
        L = []
        R = []
        for i in point_data:
            if i.get(dim) <= avg:
                L.append(i)
            else:
                R.append(i)
        return L, R, avg

    def travel(self):
        print("==================ABOUT TO TRAVEL==================")
        if self.head == None:
            print("NOTHING")
            return
        self.head.print()
        self._levelorder([self.head])
        return

    def _levelorder(self, q):
        nq = []
        if(len(q)==0):
            return
        for i in q:
            if i==None:
                print("NULL")
            else:
                i.print()
            input("")
            if type(i) == type(kd_node()):
                nq.append(i.L)
                nq.append(i.R)
            else:
                continue
        print("NEXT LEVEL")
        return self._levelorder(nq)

    def insert(self, data):
        """data is object of type point"""
        if self.head == None:
            self.head = kd_node(split_over = data.getx(), dim = 0)
            self.head.L = data.copy()
            self.count += 1
            return
        self._insert(self.head, data, 0, self.head)
        return

    def _insert(self, root, data, dim, parent):
        new_dim = (dim+1)%self.dim
        if root == None:
            """return the point object"""
            self.count += 1
            return data.copy()

        if type(root) == point:
            a = root.get(dim)
            b = data.get(dim)
            avg = (a+b)/2
            t = kd_node(split_over=avg, dim = dim, parent = parent)
            if a<b:
                t.L = root.copy()
                t.R = data.copy()
                self.count += 1
            elif a>b:
                t.L = data.copy()
                t.R = root.copy()
                self.count += 1
            else:
                """a==b==avg"""
                t.L = root.copy()
                t.L = self._insert(t.L, data, new_dim, t)
            return t
        
        if data.get(dim) <= root.split_over:
            root.L = self._insert(root.L, data, new_dim, root)
        else:
            root.R = self._insert(root.R, data, new_dim, root)
        return root

    def delete(self, data):
        """data is object of type point"""
        t = self._delete(root = self.head, data = data, pos = False, parent = None, dim = 0)
        return t

    def _delete(self, root, data, pos, dim, parent):
        new_dim = (dim+1)%self.dim
        if root == None:
            """point not found"""
            return None
        
        if type(root)==point:
            if root == data:
                """Node to be deleted found"""
                self.count -= 1
                if pos:
                    parent.R = None
                else:
                    parent.L = None
                return root.copy()
            else:
                """point object encountered but not equal to what we want hence point not found"""
                return None
        else:
            pass
        
        if data.get(dim) <= root.split_over:
            t = self._delete(root = root.L, data = data, pos = False, dim = new_dim, parent = root)
        else:
            t = self._delete(root = root.R, data = data, pos = True, dim = new_dim, parent = root)
        
        return t

    def range(self, bounds):
        """bounds is a multi array"""
        t = self._range(self.head, bounds, 0)
        return t

    def _range(self, root, bounds, dim):
        new_dim = (dim+1)%self.dim
        start = bounds[dim][0]
        end = bounds[dim][1]
        if type(root) == point:
            if(root.in_range(bounds)):
                # invoke copy constructor
                return [root.copy()]
            return []
        if start<=root.split_over<end:
            u = self._range(root.L, bounds, new_dim)
            v = self._range(root.R, bounds, new_dim)
            return u+v
        elif root.split_over>=end:
            u = self._range(root.L, bounds, new_dim)
            return u
        elif root.split_over<start:
            u = self._range(root.R, bounds, new_dim)
            return u
        else:
            raise Exception("UNEXPECTED CONDITION")

    def radius(self, p, radius):
        """function to return the number of points within a hypershere of radius r"""
        centre = p.coordinate # reference to array in object
        l = self._radius(self.head, centre, radius, 0, p)
        return l

    def _radius(self, root, centre, radius, dim, p):
        lst = []
        new_dim = (dim+1)%self.dim
        if(root == None):
            return []
        
        if type(root) == point:
            """root is point then check for its elegibilty and return suitably"""
            dist = root.distance(p)
            if 0 < dist <= radius:
                # do not include the point p
                t = root.copy()
                lst.append(t)
            return lst

        if type(root) == kd_node:
            cur_radius = root.split_over - centre[dim]
            if -radius <= cur_radius <= radius:
                """can lie in both left left subtree and left right subtree"""
                t1 = self._radius(root.L, centre, radius, new_dim, p)
                t2 = self._radius(root.R, centre, radius, new_dim, p)
                lst += t1 + t2
            elif cur_radius < -radius:
                """req'd points would lie to right"""
                t = self._radius(root.R, centre, radius, new_dim, p)
                lst += t
            elif cur_radius > radius:
                """req'd points would lie to left"""
                t = self._radius(root.L, centre, radius, new_dim, p)
                lst += t
            else:
                """req'd points would lie to left"""
                raise Exception("INVALID CONDITION WHILE DECING TO MOVE FOR HYPERSPHERE SEARCH")
        return lst

    def rough(self, data):
        """data is object of type point
        search a point which is roughly in vicinity"""
        t = self._rough(self.head, data, 0)
        return t

    def _rough(self, root, p, dim):
        """search a point which is roughly in vicinity"""
        new_dim = (dim+1)%self.dim
        if root == None:
            return None
        if type(root) == point:
            if root == p:
                return None
            return root
        if p.get(dim) > root.split_over:
            t = self._rough(root.R,p,new_dim)
            if t == None:
                t = self._rough(root.L,p,new_dim)
        else:
            t = self._rough(root.L,p,new_dim)
            if t == None:
                t = self._rough(root.R,p,new_dim)
        return t

    def search(self,data):
        if type(data) == list and len(data) == self.dim:
            return self._search(self.head, point(data), 0)
        elif type(data) == point and data.dim == self.dim:
            return self._search(self.head, data, 0)
        else:
            raise Exception("INVALID DATA TYPE TO SEARCH IN KD_TREE")
        return None

    def _search(self, root, pointData, dim):
        new_dim = (dim+1)%self.dim
        if root == None:
            return None
        if type(root) == point:
            if root == pointData:
                return root.copy()
            return None
        elif type(root) == kd_node:
            if pointData.get(dim) <= root.split_over:
                return self._search(root.L, pointData, new_dim)
            else:
                return self._search(root.R, pointData, new_dim)
        else:
            return None

    def nearest_nbr(self, data):
        """data is object of type point"""
        t = rough(data)
        arr = self.radius(t, data.distance(t))
        for i in range(len(arr)):
            arr[i] = (data.distance(arr[i]), arr[i])
        heapq.heapify(arr)
        t = heapq.nsmallest(1,arr)
        return t[0][1]

    def k_nearest_nbr_distance(self, p, distance, k):
        """list of points in a cluster within a range=distance and maximum k points"""
        t = self.radius(p, distance)
        for i in range(len(t)):
            t[i] = (p.distance(t[i]), t[i])
        heapq.heapify(t)
        t = heapq.nsmallest(k,t)
        for i in range(len(t)):
            t[i] = t[i][1]
        return t

    def _copy(self, root, parent):
        if root == None:
            return None
        if type(root) == kd_node:
            t = root.copy()
            t.P = parent
            t.L = self._copy(root.L, t)
            t.R = self._copy(root.R, t)
            return t
        if type(root) == point:
            return root.copy()
        raise Exception("INVALID DATA TYPE WHILE COPYING KD TREE")

    def copy(self):
        if self.head == None:
            return None
        tree = kd_tree(self.dim)
        tree.head = self.head.copy()
        tree.head.P = None
        tree.head.L = self._copy(self.head.L, tree.head)
        tree.head.R = self._copy(self.head.R, tree.head)
        tree.count = self.count
        return tree
    
    def get_farthest(self, data):
        '''returns the farthest point from the given point'''
        m = [(0,None)]
        self._get_farthest(self.head, data,m)
        return m[0][1]

    def _get_farthest(self, root, data, m):
        """brute force for farthest point"""
        if root == None:
            return None
        if type(root) == point:
            t = root.distance(data)
            if t > m[0][0]:
                m[0] = (t,root)
            return
        if type(root) == kd_node:
            self._get_farthest(root.L, data, m)
            self._get_farthest(root.R, data, m)
            return
        raise Exception("INAVLID DATA TYPE WHILING GETTING FARTHEST POINT")

    def smallestPoint(self):
        t = self._smallestPoint(self.head)
        return t

    def _smallestPoint(self, root):
        if root == None:
            return None
        if type(root) == point:
            return root.copy()
        l = self._smallestPoint(root.L)
        if type(l) == point:
            return l
        r = self._smallestPoint(root.R)
        return r



# driver code
'''obj = kd_tree(2)
arr = []
arr.append(point(name=1, dim=2, coordinate=[1,1]))
arr.append(point(name=2, dim=2, coordinate=[1,2]))
arr.append(point(name=5, dim=2, coordinate=[2,1]))
arr.append(point(name=6, dim=2, coordinate=[2,2]))
arr.append(point(name=9, dim=2, coordinate=[3,1]))
arr.append(point(name=10, dim=2, coordinate=[3,2]))
arr.append(point(name=11, dim=2, coordinate=[3,3]))
arr.append(point(name=12, dim=2, coordinate=[3,4]))
arr.append(point(name=7, dim=2, coordinate=[2,3]))
arr.append(point(name=8, dim=2, coordinate=[2,4]))
arr.append(point(name=4, dim=2, coordinate=[1,4]))
arr.append(point(name=3, dim=2, coordinate=[1,3]))
arr.append(point(name=13, dim=2, coordinate=[4,1]))
arr.append(point(name=14, dim=2, coordinate=[4,2]))
arr.append(point(name=15, dim=2, coordinate=[4,3]))
arr.append(point(name=16, dim=2, coordinate=[4,4]))
obj.build(arr)
#obj.travel()
#bounds = [[2,2],[3.2,3.7]]
#t = obj.k_nearest_nbr_distance(arr[3],1,2)
print("=======")
for i in t:
    i.print()'''

'''arr = []
cid = 0
a = 4
for i in range(1):
    for j in range(1):
        for k in range(a):
            arr.append(point([i,j,k],name=cid))
            cid+=1
obj = kd_tree(3)
obj.build(arr)
print("DONE")
obj.travel()
print("COUNT->",obj.count)'''