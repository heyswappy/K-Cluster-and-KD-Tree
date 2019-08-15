from point import point
from kd_tree import kd_tree
from graph import myGraph
        
def driver1():
    obj = kd_tree(2)
    arr = []
    cid = 0
    for i in range(0,10):
        for j in range(0,10):
            arr.append(point(name=cid, dim=2, coordinate=[i,j]))
            cid += 1
    swap = myGraph(2)
    for i in arr:
        t = swap.insertNode(i, key=i.name, cost=0)

    t = swap.k_center_main(10,2)
    swap.plot()


def driver2():
    obj = kd_tree(3)
    arr = []
    cid = 0
    for i in range(0,15):
        for j in range(0,15):
            for k in range(0,15):
                arr.append(point(name=cid, dim=3, coordinate=[i,j,k]))
                cid += 1
    swap = myGraph(3)
    for i in arr:
        t = swap.insertNode(i, key=i.name, cost=0)
    input("ABOUT TO CALL K CENTER")
    t = swap.k_center_main(100,10)
    print("k_center complete")
    swap.plot3()


driver1()
input("")
