import networkx as nx
from geopy import distance
from database.DAO import DAO


class Model:
    def __init__(self):
        self._listSightings = []
        self._listShapes = []
        self._listStates = []

        self._graph = nx.Graph()
        self._nodes = []
        self._edges = []

        self.solBest = 0
        self.path = []
        self.path_edge = []

        self.loadSightings()
        self.loadStates()

    def loadSightings(self):
        self._listSightings = DAO.getAllSighting()

    def loadStates(self):
        self._listStates = DAO.getAllStates()

    @property
    def listSightings(self):
        return self._listSightings

    @property
    def listStates(self):
        return self._listStates

    def searchPath(self):
        self.path = []
        self.path_edge = []

        for n in self.get_nodes():
            parziale = []
            parziale.append(n)
            self.ricorsione(parziale, [])

    def ricorsione(self, parziale, parziale_archi):
        nodoLast = parziale[-1]

        archiViciniAmmissibili = self.getArchiViciniAmm(nodoLast, parziale_archi)
        if len(archiViciniAmmissibili) == 0:
            weight_path = self.computeWeigthPath(parziale_archi)
            if weight_path > self.solBest:
                self.solBest = weight_path + 0.0
                self.path = parziale[:]
                self.path_edge = parziale_archi[:]
            return

        for a in archiViciniAmmissibili:
            parziale_archi.append((nodoLast, a, self._graph.get_edge_data(nodoLast, a)['weight']))
            parziale.append(a)

            self.ricorsione(parziale, parziale_archi)
            parziale.pop()
            parziale_archi.pop()

    def getArchiViciniAmm(self, nodoLast, parziale_archi):
        archiVicini = self._graph.edges(nodoLast, data=True)
        result = []
        for a1 in archiVicini:
            if len(parziale_archi) != 0:
                if a1[2]['weight'] > parziale_archi[-1][2]:
                    result.append(a1[1])
            else:
                result.append(a1[1])
        return result

    def computeWeigthPath(self, myList):
        weight = 0
        for e in myList:
            weight += distance.geodesic((e[0].lat, e[0].lng), (e[1].lat, e[1].lng)).km
        return weight

    def get_distance_weight(self, e):
        return distance.geodesic((e[0].lat, e[0].lng), (e[1].lat, e[1].lng)).km

    def buildGraph(self, year, shape):
        self._graph.clear()

        for state in self._listStates:
            self._nodes.append(state)

        self._graph.add_nodes_from(self._nodes)

        self.idMap = {}
        for n in self._nodes:
            self.idMap[n.id] = n

        edges = DAO.getAllNeighbors(year, shape)
        for edge in edges:
            self._edges.append((self.idMap[edge[0]], self.idMap[edge[1]], edge[2]))

        self._graph.add_weighted_edges_from(self._edges)

    def weight_edges(self):
        self._weight = []
        for n in self._graph.nodes():
            peso = 0
            for e in self._graph.edges(n, data=True):
                peso += e[2]['weight']
            self._weight.append((n.id, peso))

        return self._weight

    def get_nodes(self):
        return self._graph.nodes()

    def get_edges(self):
        return self._graph.edges()

    def get_num_nodes(self):
        return self._graph.number_of_nodes()

    def get_num_edges(self):
        return self._graph.number_of_edges()

    def getGraphDetails(self):
        return len(self._nodes), len(self._edges)


"""

FillDD classic
Query per gli archi con in ingresso anno e forma che restituisce i due nodi e il peso
idMap gestita nel Model

"""