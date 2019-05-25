from random import random
from math import e, pi
from tkinter import *


###############################################################################################################
# Tkinter
haut, larg = 600, 900

edges = dict()
fenetre = Tk()

###############################################################################################################
# Main classes

class Vertex:
    """Representation of a vertex by its ID, its coords on the circle and its adjacency list.
         The attributes edges and way are used during the function to find an Euler tour"""
    
    
    def __init__(self, idNumb):
        self.id = idNumb
        self.coordX = 0
        self.coordY = 0
        self.adjacency = []
        self.edges = []
        self.way = []
    
        
    def __str__(self):
        return str(self.id)


    def __repr__(self):
        return str(self.id)


    def __int__(self):
        return int(self.id)

        
    def getCoord(self, sizeGraph):
        """Update the coords of the vertex for the display."""

        z = (haut/2-50)*e**(pi*2j*self.id/sizeGraph)
        self.coordX = larg/2+z.real
        self.coordY = haut/2+z.imag


    def getDegree(self):

        """Returns the degree of the vertex"""
        return len(self.adjacency)




class Graph:
    """Representation of a graph by its size, its list of vertices and the probability for each edge to exist"""
	
    def __init__(self, probaEdge):
        self.size = 0
        self.verticesList = []

        
    def addVertex(self, n = 1):
        """Add n vertices to the graph"""
        
        for i in range(n):
            self.verticesList.append(Vertex(i))
        self.size += n


    def drawGraph(self):
        """Draws the graph in a canvas, each vertex being on a circle sorted by its id"""
        global edges
        
        canvas.delete("all")        
        for v in self.verticesList :
            v.getCoord(self.size)
            canvas.create_oval(v.coordX-5, v.coordY-5, v.coordX+5, v.coordY+5, fill = "blue")
            z = (haut/2-35)*e**(pi*2j*v.id/self.size)
            x, y = larg/2+z.real, haut/2+z.imag
            canvas.create_text(x, y, text = str(v))

        edges = dict()
        for v in self.verticesList:
            for idNumb in v.adjacency:
                if idNumb > v.id:
                    edges[str(v.id)+" "+str(idNumb)] = canvas.create_line(v.coordX, v.coordY, self.verticesList[idNumb].coordX, self.verticesList[idNumb].coordY, fill = "red")


    def addEdge(self, i, j):
        """Adds an edge between the vertices i and j"""
        
        self.verticesList[i].adjacency.append(j)
        self.verticesList[i].edges.append(True)
        self.verticesList[j].adjacency.append(i)
        self.verticesList[j].edges.append(True)


    def isConnected(self):
        """Returns whether the graph is connected or not"""
        
        # If there's a vertex of degree 0, the graph can't be connected
        if not all([vertex.getDegree() != 0 for vertex in self.verticesList]):
            return False
        
        checked = set()
        vertexToAnalyze = [self.verticesList[0]]
        while len(vertexToAnalyze) != 0 and len(checked) < self.size:
			
			# Analyze the next vertex and tag it checked
            vertex = vertexToAnalyze.pop(0)
            checked.add(vertex.id)
            
            # For each neighbor of vertex, if this neighbor hasn't been checked and is not to be
            # then add this neighbor to the list of vertex to analyze
            for v in vertex.adjacency:
                if v not in checked and self.verticesList[v] not in vertexToAnalyze:
                    vertexToAnalyze.append(self.verticesList[v])
        
        # If n vertices has been analyzed, then the graph is connected
        return self.size == len(checked)


    def existsTour(self):
        """Returns whether the graph is Eulerian or not"""
        return self.isConnected() and all([vertex.getDegree()%2 == 0 for vertex in self.verticesList])


    def findCycle(self, begin = 0):
        """Returns a cycle in the graph from the vertex #begin"""

		# Resets the attribute way of each vertex
        for v in self.verticesList:
            v.way = []
            
        checked = set()
        vertexToAnalyze = [self.verticesList[begin]]
        for n in range(self.size+5):
			
			# Analyze the next vertex and tag it checked
            vertex = vertexToAnalyze.pop(0)
            checked.add(vertex.id)
            
            # For each neighbor of Vertex, if :
            # - this neighbor hasn't been checked 
            # - the edge from Vertex to this neighbor hasn't been already used during the Eulerian tour
            # - Vertex and the neigbor are on two different branches of the course made until here,
			#		ie. the first vertex of their way are differents
			# Then if this neighbor already has been visited it means a cycle has been found : we return this cycle from the neighbor's way
			# Else, update the neighbor's way and add this neighbor to the list of vertex to analyze
            for w in vertex.adjacency:
                if w not in checked and vertex.edges[vertex.adjacency.index(w)] and \
                (len(vertex.way) <= 1 or len(self.verticesList[w].way) <= 1 or self.verticesList[w].way[1] != vertex.way[1]):
                    v = self.verticesList[w]
                    if v.way != []:
                        return v.way + [v.id, vertex.id] + vertex.way[::-1]
                    else:
                        v.way = vertex.way + [vertex.id]
                    vertexToAnalyze.append(v)


    def findEulerianTour(self):
        """Returns an Eulerian tour in the graph by calling the recursive function"""

        if not self.existsTour():
            return "There's no Eulerian tour in this graph"

        else:
            return self.findEulerianTourAux(0)


    def findEulerianTourAux(self, vertex):
        """Recursive function to find an Eulerian tour, based on the demonstration of Euler's theorem"""

        # Base case :
        # if every edge from Vertex has been used in the tour, just returns vertex's id
        if True not in self.verticesList[vertex].edges:
            return [vertex]

        # Recursion :
        # Find a cycle from vertex
        cycle = self.findCycle(vertex)

		# Update the edges used in this cycle : they are now tagged as used
        for i in range(len(cycle)-1):
            v = self.verticesList[cycle[i]]
            index =  v.adjacency.index(cycle[i+1])                  # Index of the vertex \cycle[i+1]\ in the adjacency list of the vertex \cycle[i]\
            v.edges[index] = False
            
            v = self.verticesList[cycle[i+1]]
            index = v.adjacency.index(cycle[i])
            v.edges[index] = False            

		# For each vertex of this cycle, find another cycle from this vertex
        tour = []
        for i in range(0, len(cycle)):
            tour.extend(self.findEulerianTourAux(cycle[i]))

        return tour
        
            



###############################################################################################################
# Main

def createGraph(n = 50, p = 0.25):
    """Returns a random graph of n vertices with an edge probability of p"""

    graph = Graph(p)
    graph.addVertex(n)
    for i in range(n):
        for j in range(i+1, n):
            if random() < p:
                graph.addEdge(i, j)
    return graph


def makeEulerian(graph):
    """Add edges to graph until it gets Eulerian"""

    if graph.size <= 2:
        print("This graph is too small to be Eulerian !")

    # Manage the vertices of degree n-1 by removing edges from these vertices
    complete = [vertex for vertex in graph.verticesList if vertex.getDegree() == graph.size-1]
    for vertex in complete:
        # Choose in priority neighbors of odd degree
        index = sorted(vertex.adjacency, key = lambda v:graph.verticesList[v].getDegree()%2 == 0)[0]
        indNeighbor = vertex.adjacency.index(index)
        indVertex = graph.verticesList[index].adjacency.index(vertex.id)        
        
        # Remove the neighbor from the adjacency list of vertex
        vertex.adjacency.pop(indNeighbor)
        vertex.edges.pop(indNeighbor) 

        # Remove Vertex from the adjacency list of the neighbor
        graph.verticesList[index].adjacency.pop(indVertex)
        graph.verticesList[index].edges.pop(indVertex)


    # Manage the vertices of odd degree (and the vertices of degree 0)
    oddDegreeVertices = [vertex for vertex in graph.verticesList if vertex.getDegree()%2 == 1 or vertex.getDegree() == 0]
    oddDegreeVertices.sort(key = lambda vertex:len([1 for v in vertex.adjacency if v in oddDegreeVertices]))
    
    while oddDegreeVertices != []:
        vertex = oddDegreeVertices.pop(0)
        
        # Filter the possibles vertices to link with Vertex (ie. the vertices not already linked with Vertex, and with an odd or a null degree)
        possiblesVertices = list(filter(lambda v:v.id not in vertex.adjacency, oddDegreeVertices))
        
        # If there is such a vertex, create an edge between Vertex and this neighbor and remove it from oddDegreeVertices (unless it had a null degree)
        if possiblesVertices != []:
            neighbor = possiblesVertices[0]
            graph.addEdge(vertex.id, neighbor.id)
            if neighbor.getDegree() != 1:
                oddDegreeVertices.remove(neighbor)
                
        else:
			# If there isn't such a vertex, consider the vertices with an even degree not linked with Vertex
            possiblesVertices = list(filter(lambda v:v.id not in vertex.adjacency and v.id != vertex.id and v.getDegree() < graph.size-2, graph.verticesList))
            
            # If there is such a vertex, create an edge between Vertex and this neighbor and add it to oddDegreeVertices (because it now has an odd degree)
            if possiblesVertices != []:
                neighbor = possiblesVertices[0]
                oddDegreeVertices.append(neighbor)
                graph.addEdge(vertex.id, neighbor.id)
            
            # If none of these vertices can be linked, it means that edges have to be removed instead of added (with priority on neighbors with an odd degree)
            else:
                print(vertex.id, vertex.adjacency, graph.verticesList)
                for v in graph.verticesList:
                    print(str(v) + " : " + ", ".join(map(str, v.adjacency)))
                index = sorted(vertex.adjacency, key = lambda v:graph.verticesList[v].getDegree()%2 == 0)[0]
                indNeighbor = vertex.adjacency.index(index)
                indVertex = graph.verticesList[index].adjacency.index(vertex.id)
                
                # Remove the neighbor from the adjacency list of Vertex
                vertex.adjacency.pop(indNeighbor)
                vertex.edges.pop(indNeighbor)
                
                # Remove Vertex from the adjacency list of the neighbor
                graph.verticesList[index].adjacency.pop(indVertex)
                graph.verticesList[index].edges.pop(indVertex)
                
                # If the neighbor had an odd degree, it now has an even degree so it has to be removed from oddDegreeVertices
                if graph.verticesList[index].getDegree()%2 == 0:
                        oddDegreeVertices.remove(graph.verticesList[index])

        # If vertex had a degree 0, it must remain in oddDegreeVertices
        if vertex.getDegree() == 1:
            oddDegreeVertices.append(vertex)



###############################################################################################################
# Example

# g = createGraph(35, 0.125)
# print("The graph is connected : ", g.isConnected())
# print("The graph has an Eulerian tour : ", g.existsTour())

# for v in g.verticesList:
    # print(str(v) + " : " + ", ".join(map(str, v.adjacency)))

# if not g.existsTour():
    # makeEulerian(g)

# print("After modification , the graph has an Eulerian tour : ", g.existsTour())
# for v in g.verticesList:
    # print(str(v) + " : " + ", ".join(map(str, v.adjacency)))

# way = g.findEulerianTour()
# print(way)

# print("Size of the tour : ", len(way)-1)
# print("Number of edges :", sum([v.getDegree() for v in g.verticesList])//2)



###############################################################################################################
# Fonctions Tkinter

graph = []
indice = 0
tour = []

def maj(graph):
    """Update the tkinter"""

    graph.drawGraph()
    connected.config(text = "Connected : " + str(graph.isConnected()), fg = "green" if graph.isConnected() else "red")
    eulerian.config(text = "Eulerian : " + str(graph.existsTour()), fg = "green" if graph.existsTour() else "red")

def generate():
    """Generates a new random graph and displays it"""
    global graph

    try:
        n = int(entryVertices.get())
        p = float(entryProba.get())
        assert(2 < n and 0 <= p <= 1)
        action.grid_remove()
        graph = createGraph(n, p)
        maj(graph)
        nextEdgeEuler.grid_remove()
        drawEulerTour.grid(row = 4, column = 5, columnspan = 6)
    
    except (ValueError, AssertionError):
        action.grid(row = 3, column = 5, columnspan = 2)


def makeEuler():
    """Modify a graph to make it eulerian"""
    global graph

    if type(graph) == Graph and 2 < graph.size:
        makeEulerian(graph)
        maj(graph)


def drawEuler():
    """Display an Euler tour"""
    global graph, itera, tour

    tour = graph.findEulerianTour()
    drawEulerTour.grid_remove()
    nextEdgeEuler.grid(row = 4, column = 5, columnspan = 2)
    itera = nextEuler(tour)


def nextEuler(tour):
    """Display the next edge of tour"""
    global graph

    for i in range(len(tour)-1):
        if tour[i] < tour[i+1]:
            canvas.itemconfig(edges[str(tour[i])+" "+str(tour[i+1])], fill = "green")
        else:
            canvas.itemconfig(edges[str(tour[i+1])+" "+str(tour[i])], fill = "green")
        yield


def nextEulerEnd():
    global graph, itera

    try:
        next(itera)
    except StopIteration:
        nextEdgeEuler.grid_remove()
        drawEulerTour.grid(row = 4, column = 5, columnspan = 2)


canvas = Canvas(fenetre, width = larg, height = haut, bg = "white")
canvas.grid(row = 2, column = 1, rowspan = 3, columnspan = 4)

connected = Label(fenetre, text = "Connected")
connected.grid(row = 5, column = 3)

eulerian = Label(fenetre, text = "Eulerian")
eulerian.grid(row = 5, column = 2)

vertices = Label(fenetre, text = "Number of vertices")
vertices.grid(row = 1, column = 1, sticky = E)

proba = Label(fenetre, text = "Probability for edges")
proba.grid(row = 1, column = 3, sticky = E)

entryVertices = Entry(fenetre)
entryVertices.grid(row = 1, column = 2)

entryProba = Entry(fenetre)
entryProba.grid(row = 1, column = 4)

action = Label(fenetre, text = "Enter a valid number of vertices\nand a valid probability", bg = "red")
action.grid(row = 3, column = 5, columnspan = 2)

new_graph = Button(fenetre, text = "Generate a new graph", command = generate)
new_graph.grid(row = 2, column = 5, sticky = S)

make_euler = Button(fenetre, text = "Make the graph Eulerian", command = makeEuler)
make_euler.grid(row = 2, column = 6, sticky = S)

drawEulerTour = Button(fenetre, text = "Draw an Eulerian tour", command = drawEuler)
drawEulerTour.grid(row = 4, column = 5, columnspan = 2)

nextEdgeEuler = Button(fenetre, text = "Next", command = nextEulerEnd)

fenetre.mainloop()
