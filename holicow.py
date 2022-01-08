"""
description: a puzzle game
language: python3
author: Lahari Chepuri(lc8104 @ RIT.EDU)
author: Smita Subhadarshinee Mishra(sm8528 @ RIT.EDU)
"""

import sys
from os import path
from math import sqrt

class Cow:
    """
    Stores cow objects
    """
    __slots__ = "type", "name", "x", "y", "painted"

    def __init__(self, name, x, y):
        self.type = "cow"
        self.name = name
        self.x = x
        self.y = y
        self.painted = []

    def __str__(self):
        """
        creates a string representation of the cow object
        :return: string representation of the cow object
        """
        return self.name + ": (" +str(self.x )+ ", "+str(self.y) + ") " + str(self.painted)

class PaintBall:
    """
    Stores paint ball objects
    """
    __slots__ = "type", "name", "x", "y","radius"

    def __init__(self, color, x, y, rad):
        self.type = "paintball"
        self.name = color.upper()
        self.x = x
        self.y = y
        self.radius = rad

    def __str__(self):
        """
        creates a string representation of the paint ball object
        :return: string representation of the paint ball object
        """
        return self.name + ": (" +str(self.x) + ", "+str(self.y) + ") " + str(self.radius)

class Vertex:
    """
    Stores all the vertices of the graph
    """
    __slots__ = "object","connectedTo", "pbConnected", "cowConnected"

    def __init__(self, object):
        self.object = object
        self.connectedTo = []
        self.pbConnected = []
        self.cowConnected = []

    def add_neighbour(self, vertex):
        """
        connects the vertex to another vertex(Directed)
        :param: the vertex that needs to be connected
        """
        if vertex.object.type == "cow":
            self.cowConnected.append(vertex)
        if vertex.object.type == "paintball":
            self.pbConnected.append(vertex)
        self.connectedTo.append(vertex)

    def __str__(self):
        """
        creates a string representation of the vertex
        :return: string representation of the vertex
        """
        string = self.object.name + " connectedTo: ["
        for i in range(0,len(self.connectedTo)):
            string += self.connectedTo[i].object.name
            if i != len(self.connectedTo) - 1:
                string += ", "
        string += "]"
        return string

class Field:
    """
    Stores the main graph(Field)
    """
    __slots__ = "vertex_dict", "num_vertices", "results"

    def __init__(self):
        self.vertex_dict = {}
        self.num_vertices = 0
        self.results = {}

    def add_vertex(self, vertex):
        """
        Adds a vertex to the graph
        :param: the vertex that needs to be added
        """
        if vertex.object.name not in self.vertex_dict:
            self.num_vertices += 1
        self.vertex_dict[vertex.object.name] = vertex

    def printField(self):
        """
        prints the entire graph(Field of Dreams)
        """
        print("Field of Dreams: ")
        print("-------------------------")
        print(str(self))

    def create_cows_dict(self):
        """
        Generates a dictionary with the keys as the name of the cow
        and the values as some dummy values
        :return: the created dictionary
        """
        cows_dict = {}
        for key in self.vertex_dict:
            if self.vertex_dict[key].object.type == "cow":
                cows_dict[self.vertex_dict[key].object.name] = ""
        return cows_dict

    def __trigger(self, vertex, cows_colors, triggered):
        """
        helper method of trigger that paints the cows
        and triggers the paint ball connected to each vertex
        :param: the vertex that is to be triggered
        :param: colors that each cow is painted with on triggering that vertex
        :param: list of all the vertices that haven been triggered already
        :return: colors that each cow is painted with on triggering that vertex(Dict)
        """
        color = vertex.object.name
        if color not in triggered:
            for cow in vertex.cowConnected:
                cow.object.painted.append(color)
                col = color + "!"
                cows_colors[cow.object.name] += " " + color
                print("\t", cow.object.name, "is painted", col)
            for pb in vertex.pbConnected:
                print("\t", pb.object.name, "paint ball is Triggered by", color, "paint ball")
                triggered.append(color)
                self.__trigger(self.vertex_dict[pb.object.name], cows_colors, triggered)
            return cows_colors

    def trigger(self):
        """
        triggers each paint ball in the graph(Field)
        """
        print("Beginning simulation...")
        for key in self.vertex_dict:
            vertex = self.vertex_dict[key]
            if vertex.object.type == "paintball":
                print("Triggering", vertex.object.name, "paint ball...")
                cows_colors = self.create_cows_dict()
                triggered = []
                self.results[vertex.object.name] = self.__trigger(vertex, cows_colors, triggered)
        print()

    def displayOptimalRes(self):
        """
        prints the final(optimal) result
        """
        max = 0
        current_tot = 0
        max_color  = {}
        color = ""
        if len(self.results) == 0:
            print("There are no paint balls in the field, please place them to paint the cows!")
        else:
            for each_color in self.results:
                current_tot = 0
                if self.results[each_color] is not None:
                    for each_cow in self.results[each_color]:
                        current_tot += len(self.results[each_color][each_cow].split())
                    if current_tot > max:
                        max = current_tot
                        max_color = self.results[each_color]
                        color = each_color
            print("Results: ")
            if max == 0:
                print("No cows have been painted, because of one of the two reasons:")
                print("\t", "1. there are no cows in the field")
                print("\t", "2. you have not placed the paint balls closer to the cows")
            else:
                print("Triggering the", color, "paint ball is the best choice with", max, "total paint on the cows")
                for key in max_color:
                    result = key + "'s colors: {" + max_color[key] + " }"
                    print("\t", result)

    def __str__(self):
        """
        creates a string representation of the graph
        :return: string representation of the graph
        """
        string = ""
        for key in self.vertex_dict:
            string += str(self.vertex_dict[key]) + "\n"
        return string

def distance(x1,y1, x2, y2):
    """
    calculates distance between two points
    :return: distance between two points
    """
    return sqrt( ((x2-x1)**2) + ((y2-y1)**2) )

def create_field(cows, paintballs):
    """
    creates a graph of cows and paint balls and
    1. calls the method to print the field
    2. calls the method that triggers each paint ball
    3. calls the method that print the final result(Optimal)
    :param: a list of all cows
    :param: a list of all paint balls
    """
    field = Field()
    for cow in cows:
        field.add_vertex(Vertex(cow))
    for i in range(0, len(paintballs)):
        v = Vertex(paintballs[i])
        for cow in cows:
            dist = distance(cow.x, cow.y, paintballs[i].x, paintballs[i].y)
            if dist <= paintballs[i].radius:
                v.add_neighbour(Vertex(cow))
        for j in range(0, len(paintballs)):
            dist = distance(paintballs[i].x, paintballs[i].y, paintballs[j].x, paintballs[j].y)
            if i != j and (dist <= paintballs[i].radius):
                v.add_neighbour(Vertex(paintballs[j]))
        field.add_vertex(v)
    if len(field.vertex_dict) != 0:
        field.printField()
        field.trigger()
        field.displayOptimalRes()
    else:
        print("Place cows and paint balls in the field, the field is empty!")

def parsefile(filename):
    """
    parses the file and then calls the method that generates the graph
    :param: filename of the file that needs to be parsed
    """
    cows = []
    paintballs = []
    with open(filename) as file:
        for line in file:
            contents = line.strip().split()
            if contents[0] == "cow":
                cows.append(Cow(contents[1], int(contents[2]), int(contents[3])))
            if contents[0] == "paintball":
                paintballs.append(PaintBall(contents[1], int(contents[2]), int(contents[3]), int(contents[4])))
        create_field(cows,paintballs)

def cmd_args():
    """
    handles and parses the arguments passed through command line
    """
    if len(sys.argv)>1:
        filename = sys.argv[1].split("/")[-1]
        if path.exists(sys.argv[1]):
            if path.isfile(sys.argv[1]):
                parsefile(sys.argv[1])
            else:
                print("File not found:", filename)
        else:
            print("File not found:", filename)
    else:
        pyfilename = sys.argv[0].split("/")[-1]
        print("usage: python3",pyfilename, "{filename}")
        sys.exit()

def main():
    cmd_args()

if __name__ == '__main__':
    main()