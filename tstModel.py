from model.model import Model

mymodel=Model()
mymodel.buildGraph()

print(f"Il grafico ha {mymodel.getNumNodes()} nodi.")   #double check nella query "select count(*) from fermata f"
print(f"Il grafico ha {mymodel.getNumEdges()} archi.")