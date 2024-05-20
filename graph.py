import matplotlib.pyplot as plt
import networkx as nx


def plot(graph1, graph2):

    plt.figure(figsize=(10, 6))
    nx.draw(graph1, with_labels=True, node_color="lightblue", edge_color="gray")
    plt.title("Code 1 Graph")
    plt.show()

    plt.figure(figsize=(10, 6))
    nx.draw(graph2, with_labels=True, node_color="lightgreen", edge_color="gray")
    plt.title("Code 2 Graph")
    plt.show()
