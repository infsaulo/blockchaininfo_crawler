import numpy
import argparse
import networkx as nx

def transform_adjacency(graph):
    nodes_list = graph.nodes()
    adjacency_matrix = numpy.zeros((len(graph.nodes()), len(graph.nodes())))

    # Fill the adjacency matrix with the 1, as a default metric in PageRank
    for node in nodes_list:
        node_index = nodes_list.index(node)
        edges_dict = graph[node]
        factor = 1
        for node2, edge_params in edges_dict.items():
            node2_index = self.nodes_list.index(node2)
            adjacency_matrix[node2_index][node_index] = factor

    return numpy.asmatrix(adjacency_matrix)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph_filename', dest='graph_filename')
    parser.add_argument('--out', dest='out_filename')
    args = parser.parse_args()

    graph = nx.read_gpickle(args.graph_filename)
    matrix = transform_adjacency(graph)

    with open(args.out_filename) as outfile:
        for index_row in xrange(matrix.shape[0]):
            for index_column in xrange(matrix.shape[1]):
                out.write(str(matrix.item(index_row, index_column)) + " ")

            out.write("\n")

if __name__ == "__main__":
    main()