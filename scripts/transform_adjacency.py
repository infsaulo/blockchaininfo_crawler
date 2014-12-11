import numpy
import argparse
import networkx as nx

def transform_adjacency(graph):
    nodes_list = graph.nodes()
    list_edges = []

    # Fill the adjacency matrix with the 1, as a default metric in PageRank
    for node in nodes_list:
        node_index = nodes_list.index(node)
        edges_dict = graph[node]
        for node2, edge_params in edges_dict.items():
            node2_index = nodes_list.index(node2)
            list_edges.append((node_index, node2_index))

    return list_edges, nodes_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph_filename', dest='graph_filename')
    parser.add_argument('--out', dest='out_filename')
    parser.add_argument('--dictout', dest='dict_out')
    args = parser.parse_args()

    graph = nx.read_gpickle(args.graph_filename)
    list_edges, nodes_list = transform_adjacency(graph)

    with open(args.out_filename) as outfile:
        out.write("M = [\n")
	for edge in list_edges:
            out.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')
	out.write('];')

    with open(args.dict_out) as dictfile:
        for index in xrange(len(nodes_list)):
            dictfile.write(str(index) + ' ' + str(nodes_list[index]) + '\n')

if __name__ == "__main__":
    main()
