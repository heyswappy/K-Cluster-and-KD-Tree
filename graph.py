from point import point
from kd_tree import kd_tree
from node import node

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(100000)

class myGraph:
    "CLASS TO REPRESENT THE VERTICES AND EDGES OF A GRAPH"
    """static members"""
    id_count = 0
    def __init__(self, dim):
        self.graph = {}
        self.dim = dim
        self.tree = kd_tree(dim)
        self.centers = []
        return
    
    def insertNode(self, data, key=None, cost=None):
        if key not in self.graph:
            if key == None:
                if type(data) == point:
                    self.graph[myGraph.id_count] = node(myGraph.id_count, data.coordinate, cost)
                    self.tree.insert(self.graph[myGraph.id_count].point)
                elif type(data) == list:
                    self.graph[myGraph.id_count] = node(myGraph.id_count, data, cost)
                    self.tree.insert(self.graph[myGraph.id_count].point)
                else:
                    raise Exception("DATA PROVIDED WHILE INSERTING NODE MUST BE OF TYPE POINT OR LIST.")
                myGraph.id_count += 1
                return myGraph.id_count-1
            else:
                if type(data) == point:
                    self.graph[key] = node(key, data.coordinate, cost)
                    self.tree.insert(self.graph[key].point)
                elif type(data) == list:
                    self.graph[key] = node(key, data, cost)
                    self.tree.insert(self.graph[key].point)
                else:
                    raise Exception("DATA PROVIDED WHILE INSERTING NODE MUST BE OF TYPE POINT OR LIST.")
                myGraph.id_count = max(myGraph.id_count, key)
                myGraph.id_count += 1
                return key
        return key
    
    def deleteNode(self,key):
        if key in self.graph:
            for each in self.graph[key].nbr:
                del(self.graph[each].nbr[key])
            del(self.graph[key])
        return
    
    def insertUniEdge(self, src, dest, wt=None):
        if src in self.graph and dest in self.graph:
            self.graph[src].addNbr(dest, self.graph[dest], wt)
        return

    def insertEdge(self, src, dest, wt=None):
        if src in self.graph and dest in self.graph:
            self.graph[src].addNbr(dest, self.graph[dest], wt)
            self.graph[dest].addNbr(src, self.graph[src], wt)
        return
    
    def search(self, data):
        # where data could be coordinate list or point
        t = self.tree.search(data)
        return t
    
    def print_map(self):
        for i in self.graph:
            print("KEY:",i,end=' ')
            for j in self.graph[i].nbr:
                print(j)
    
    def _get_centre(self, point_arr):
        """find the center of cluster
        min_coordinate and max_coordinate contain the min and max of ith at ith index
        cur_center has the new centre"""
        min_coordinate = []
        max_coordinate = []
        cur_center = []
        for i in range(self.dim):
            min_coordinate.append(point_arr[0].get(i))
            max_coordinate.append(point_arr[0].get(i))
        for each in point_arr:
            for j in range(self.dim):
                min_coordinate[j] = min(min_coordinate[j],each.get(j))
                max_coordinate[j] = max(max_coordinate[j],each.get(j))
        for i in range(self.dim):
            cur_center.append((min_coordinate[i]+max_coordinate[i])/2)
        return cur_center

    def _k_center_create_cluster(self, pointData, capacity, distance, tree):
        # use the capacity/2 as the radius
        # creates a cluster where each cluster contains capacity number of points
        if pointData == None:
            return None
        point_arr = tree.k_nearest_nbr_distance(distance=distance, k=capacity-1, p=pointData)
        point_arr.append(pointData)
       
        cur_center = self._get_centre(point_arr)
        new_center = tree.search(cur_center)
        if new_center == None:
            new_center = self.insertNode(cur_center)
            new_center = self.graph[new_center].point
        else:
            pass
        self.centers.append(new_center)

        for i in point_arr:
            tree.delete(i)
            self.insertEdge(new_center.name, i.name)
        tree.delete(new_center)
        tree.delete(pointData)
        return new_center

    def k_center_main(self, cluster_size, distance):
        """groups into k centers"""
        tree = self.tree.copy()
        list_of_clusters = []
        p = tree.smallestPoint()
        #print("Smallest point is:",end=" ")
        #p.print()
        while(tree.count!=0):
            if p == None:
                raise Exception("INVALID POINT")
            t = self._k_center_create_cluster(p, cluster_size, distance, tree)
            list_of_clusters.append(t)
            last_point = self.centers[-1]
            p = tree.get_farthest(p)
            print("Remaining:",tree.count)
        return list_of_clusters
    
    def plot(self):
        x = []
        y = []
        for i in self.graph:
            x.append(self.graph[i].point.getx())
            y.append(self.graph[i].point.gety())
        plt.scatter(x, y, c="blue")
        x = []
        y = []
        co = ["red","blue","green","yellow","black"]
        ji = 0
        for i in self.centers:
            plt.scatter(i.getx(), i.gety(), s=100, c="red")
            a = self.graph[i.name].point.getx()
            b = self.graph[i.name].point.gety()
            x.append(a)
            y.append(b)
            for j in self.graph[i.name].nbr:
                c = self.graph[j].point.getx()
                d = self.graph[j].point.gety()
                u = [a,c]
                v = [b,d]
                plt.plot(u, v, c=co[ji])
            ji = (ji+1)%5
        plt.show()
    
    def plot3(self):
        fig = plt.figure()
        new_plot = fig.add_subplot(111, projection='3d')
        x = []
        y = []
        z = []
        for i in self.graph:
            x.append(self.graph[i].point.getx())
            y.append(self.graph[i].point.gety())
            z.append(self.graph[i].point.getz())
        new_plot.scatter(x, y, z, c="blue")
        x = []
        y = []
        z = []
        co = ["red","green","yellow","black"]
        ji = 0
        for i in self.centers:
            new_plot.scatter(i.getx(), i.gety(), i.getz(), s=100, c="red")
            a = self.graph[i.name].point.getx()
            b = self.graph[i.name].point.gety()
            c = self.graph[i.name].point.getz()
            x.append(a)
            y.append(b)
            z.append(c)
            for j in self.graph[i.name].nbr:
                d = self.graph[j].point.getx()
                e = self.graph[j].point.gety()
                f = self.graph[j].point.getz()
                u = [a,d]
                v = [b,e]
                w = [c,f]
                new_plot.plot(u, v, w, c=co[ji])
            ji = (ji+1)%4
        plt.show()
