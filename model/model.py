from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMap={}
        for f in self._fermate:
            self._idMap[f.id_fermata]= f

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgePesati()

    def getArchiPesoMaggiore(self):
     if len(self._grafo.edges)==0:
        print("Il grafo è vuoto")
        return
     edges= self._grafo.edges()
     result = []
     for u,v in edges:
        peso=self._grafo[u][v]["weight"]  #accesso al dizionario
        if peso>1:
             result.append((u,v,peso))

     return result

    def getBFSNodes(self,source):    #conviene per i cammini minimi
         edges=nx.bfs_edges(self._grafo,source)
         visited = []
         for u,v in edges:
            visited.append(v)
         return visited

    def getDFSNodes(self,source):   #conviene per cercare una componente connessa
        edges=nx.dfs_edges(self._grafo,source)
        visited = []
        for u, v in edges:
            visited.append(v)
        return visited

    def buildGraph(self):
        self._grafo.add_nodes_from(self._fermate)
        #Mode 1:doppio loop su nodi e query per ogni arco SOLO CON POCHI NODI
        """for u in self._fermate:
            for v in self._fermate:
                res = DAO.getEdge(u,v)
                if len(res) > 0:
                    self._grafo.add_edge(u,v)
                    print(f"Added edge between {u} and {v} to graph")"""
        #Mode 2: loop singolo sui nodi e query per identificare i vicini
        """for u in self._fermate:
            vicini=DAO.getEdgesVicini(u)
            for v in vicini:
                v_nodo=self._idMap[v.id_stazA]
                self._grafo.add_edge(u,v)
                print(f"Added edge between {u} and {v_nodo} to graph")"""
        #Mode 3: unica query che legge tutte le connessioni
        allConnessioni=DAO.getAllConnessioni()
        print(len(allConnessioni))
        for c in allConnessioni:
            u_nodo= self._idMap[c.id_stazP]
            v_nodo = self._idMap[c.id_stazA]
            self._grafo.add_edge(u_nodo,v_nodo)

    def addEdgePesati(self):
        self._grafo.clear_edges()
        allConnessioni=DAO.getAllConnessioni()
        for c in allConnessioni: #peso= numero di volte che ho aggiunto arco
            if self._grafo.has_edge(self._idMap[c.id_stazP],self._idMap[c.id_stazA]):
                self._grafo[self._idMap[c.id_stazP]][self._idMap[c.id_stazA]]["weight"]+=1
            else:
                self._grafo.add_edge(self._idMap[c.id_stazP], self._idMap[c.id_stazA],weight=1)

    def getEdgeWeight(self,v1,v2):
        return self._grafo[v1][v2]["weight"]


    @property
    def fermate(self):
        return self._fermate

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
       return len(self._grafo.edges)