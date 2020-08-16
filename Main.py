import networkx as nx
import matplotlib.pyplot as plt

def reverse_delete():
    # sort the edges by their weigt, then reverse it to become buttom-up
    # start deleting from the first index, each edge that makes the graph disconnected by getting deleted, is a
    # MST edge.
    given_graph = main_graph.copy(as_view=False)
    mst_weight = 0
    mst_edges = []
    given_edges = sorted(given_graph.edges(data=True), key=lambda x: x[2]['weight'])
    given_edges.reverse()
    for each_edge in given_edges:
        given_graph.remove_edge(each_edge[0], each_edge[1])
        if nx.is_connected(given_graph) is False:
            given_graph.add_edge(each_edge[0], each_edge[1])
            mst_edges.append(each_edge)
            mst_weight += each_edge[2]['weight']
    print("MST EDGES : ", mst_edges)
    print("MST WEIGHT : ", mst_weight)
    return given_graph

def createAdjMatrix():
    inp_graph = nx.adjacency_matrix(main_graph)
    inp_graph = inp_graph.todense()
    out_matrix = []
    for i in range(nx.number_of_nodes(main_graph)):
        out_matrix.append(inp_graph[i].tolist()[0])
    return out_matrix

def prim():
    # start from an arbitrary node, in this case, the firt one, and use the adjacency system to find the adjacent nodes
    # with the lowest weight in the whole edged team, till we all the edges get visited.
    adjMatrix = createAdjMatrix()
    vertex = 0
    MST = []
    edges = []
    visited = []
    minEdge = [None, None, float('inf')]

    while len(MST) != nx.number_of_nodes(main_graph) - 1:
        visited.append(vertex)
        for r in range(0, nx.number_of_nodes(main_graph)):
            if adjMatrix[vertex][r] != 0:
                edges.append([vertex, r, adjMatrix[vertex][r]])
        for e in range(0, len(edges)):
            if edges[e][2] < minEdge[2] and edges[e][1] not in visited:
                minEdge = edges[e]
        edges.remove(minEdge)
        MST.append(minEdge)
        vertex = minEdge[1]
        minEdge = [None, None, float('inf')]

    return MST

def graph_mst_print(given_graph, mst_edges, flag):
    if flag is True:
        main_edges = [(u, v) for (u, v, d) in given_graph.edges(data=True)]
        mst_edges = [(u, v) for (u, v, d) in mst_edges.edges(data=True)]
    else:
        mst_weight = 0
        for i in range(len(mst_edges)):
            mst_weight += mst_edges[i][2]['weight']
        print("MST EDGES : ", mst_edges)
        print("MST WEIGHT : ", mst_weight)
        main_edges = [(u, v) for (u, v, d) in given_graph.edges(data=True)]
        mst_edges = [(u + 1, v + 1) for (u, v, d) in mst_edges]
    main_edges_cleaned = []
    for each in main_edges:
        if each not in mst_edges and (each[1], each[0]) not in mst_edges:
            main_edges_cleaned.append(each)
    pos = nx.spring_layout(main_graph)
    nx.draw_networkx_nodes(given_graph, pos, node_size=700)
    nx.draw_networkx_edges(given_graph, pos, edgelist=main_edges_cleaned, width=6)
    nx.draw_networkx_edges(given_graph, pos, edgelist=mst_edges, width=6, alpha=0.5, edge_color='b', style='dashed')
    nx.draw_networkx_labels(given_graph, pos, font_size=20, font_family='sans-serif')
    plt.axis('off')
    plt.title(("(REVERSE-DELETE) " if flag is True else "(PRIM) ") + "Straight Line : Main Graph / Dashed Line : MST")
    plt.show()


# this is where the main code begins and it makes the graph using the networkX library
# then you gotta choose whhich algorithm to run on this graph
# you have two Algoritm choices : 1- REVERSE DELETE 2- PRIM

main_graph = nx.Graph()
edges_count = int(input("Edges Count: "))
print("Enter", edges_count, "the edges: (Example: 5 8 30)")
for i in range(edges_count):
    new_edge = input()
    ne_parts = new_edge.split(" ")
    i_edge = int(ne_parts[0])
    j_edge = int(ne_parts[1])
    edge_weight = int(ne_parts[2])
    main_graph.add_edge(i_edge, j_edge, weight=edge_weight)

while True:
    order = int(input("1- Show Info 2- Reverse-Delete 3- Prim 4- Display 5- Exit \n"))
    if order == 1:
        print(nx.info(main_graph))
    if order == 2:
        mst_graph = reverse_delete()
        graph_mst_print(main_graph, mst_graph, True)
    if order == 3:
        presult = prim()
        pfinal = []
        for i in range(len(presult)):
            pfinal.append((presult[i][0], presult[i][1], {'weight': presult[i][2]}))
        graph_mst_print(main_graph, pfinal, False)
    if order == 4:
        nx.draw_networkx(main_graph)
        plt.axis('off')
        plt.show()
    if order == 5:
        break

# 1 2 7
# 2 3 8
# 1 4 5
# 2 4 9
# 2 5 7
# 3 5 5
# 4 5 15
# 4 6 6
# 5 6 8
# 6 7 11
# 5 7 9