class Vertex:

    __slots__ = "id", "connected_to"

    def __init__(self, key):
        self.id = key
        self.connected_to = {}

    def addNeighbour(self, nbr, weight = 0):
        #addNeighbour for directed graph
        self.connected_to[nbr] = weight
        #for undirected graph you invoke addNeighbour method on that value.

    def __str__(self):
        return str(self.id) + ' Connected to: ' + str([str(x.id) for x in self.connected_to])

    def getConnections(self):
        return self.connected_to.keys()

    def getWeight(self, nbr):
        return self.connected_to[nbr]

class Graph:

    __slots__ =  "vertex_dict","num_vertices"

    def __init__(self):
        self.num_vertices = 0
        self.vertex_dict = {}

    def addVertex(self, key):
        #if the val is not present, add a new one
        if key not in self.vertex_dict:
            self.vertex_dict[key] = Vertex(key)
            self.num_vertices += 1
        #else, just retrieve the old one
        else:
            return self.vertex_dict[key]

    def getVertex(self, key):
        if key in self.vertex_dict:
            return self.vertex_dict[key]
        return None

    def __contains__(self, key):
        return key in self.vertex_dict

    def addEdge(self, src, dest, cost=0):
        if src not in self.vertex_dict:
            self.vertex_dict[src] = Vertex(src)
        if dest not in self.vertex_dict:
            self.vertex_dict[dest] = Vertex(dest)
        self.vertex_dict[src].addNeighbour(self.vertex_dict[dest],cost)

def test():
    a = Vertex(1)
    b = Vertex(2)
    c = Vertex('b')

    a.addNeighbour(c)
    a.addNeighbour(b)

    print(a)

if __name__ == '__main__':
    test()
