import numpy
from sys import maxint


class PageRank:

    def __init__(self, graph, dumping_factor, min_quadratic_error):
        self.dumping_factor = dumping_factor
        self.min_quadratic_error = min_quadratic_error
        self.nodes_list = graph.nodes()
        self.adjacency_matrix = self.get_adjacency_matrix(graph)
        self.surfer_random_walk_matrix = (1.0 - dumping_factor) / self.adjacency_matrix.shape[0] * \
                                         numpy.asmatrix(numpy.ones((self.adjacency_matrix.shape[0], 1)))

    # graph is a networkx Graph or DiGraph instance
    def get_adjacency_matrix(self, graph):
        adjacency_matrix = numpy.zeros((len(self.nodes_list), len(self.nodes_list)))

        # Fill the adjacency matrix with the 1/outdegree(node), as a default metric in PageRank
        for node in self.nodes_list:
            node_index = self.nodes_list.index(node)
            edges_dict = graph[node]
            if edges_dict:
                factor = 1.0 / len(edges_dict)
                for node2, edge_params in edges_dict.items():
                    node2_index = self.nodes_list.index(node2)
                    adjacency_matrix[node2_index][node_index] = factor
            else:
                factor = 1.0
                adjacency_matrix[node_index][node_index] = factor

        return numpy.asmatrix(adjacency_matrix)

    # Graph is a digraph
    def run(self):

        # Initializing page_rank scores as 1/N where N is the amount of pages. This is an uniform distribution
        page_rank_column_vector = 1.0 / self.adjacency_matrix.shape[0] * \
                                  numpy.asmatrix(numpy.ones((self.adjacency_matrix.shape[0], 1)))

        last_page_rank_column_vector = maxint * numpy.asmatrix(numpy.ones((self.adjacency_matrix.shape[0], 1)))

        # Convergence condition
        while(numpy.linalg.norm(page_rank_column_vector - last_page_rank_column_vector) > self.min_quadratic_error):
            last_page_rank_column_vector = page_rank_column_vector
            page_rank_column_vector = self.surfer_random_walk_matrix + \
                                      self.dumping_factor * self.adjacency_matrix * page_rank_column_vector

        page_rank_dict = dict()
        for index in xrange(len(self.nodes_list)):
            page_rank_dict[self.nodes_list[index]] = page_rank_column_vector.item(index, 0)

        return page_rank_dict