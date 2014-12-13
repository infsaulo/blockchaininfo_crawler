import numpy
import argparse
import networkx as nx
from threading import Thread


class Gauss_Jacobi_Threaded_Iterator(Thread):

    def __init__(self, range_nodes, graph, nodes_list, X_last, X):
        Thread.__init__(self)
        self.range_nodes = range_nodes
        self.graph = graph
        self.nodes_list = nodes_list
        self.X_last = X_last
        self.X = X

    def run(self):
        for index in xrange(self.range_nodes[0], self.range_nodes[1]):
            print "Getting k predecessors of " + str(index)
            list_dict_adjacencies = self.graph.predecessors(self.nodes_list[index])
            print "Got k predecessors of " + str(index)
            value = 0.0
            for node in list_dict_adjacencies:
                node_index = self.nodes_list.index(node)
                value += (1.0/len(list_dict_adjacencies)) * self.X_last[node_index, 0]
            self.X[index] = value


def gauss_jacobi_iterate_threaded(graph, nodes_list, X_last):

    X = numpy.asmatrix(numpy.empty((X_last.shape[0], 1)))
    threaded_iterators = []
    slot_size = 1000
    number_threaded_iterators = X_last.shape[0]/ slot_size
    for index in xrange(number_threaded_iterators):
        threaded_iterators.append(
            Gauss_Jacobi_Threaded_Iterator((index*slot_size, index*slot_size + slot_size),
                                           graph, nodes_list, X_last, X))

    for index in xrange(number_threaded_iterators):
        threaded_iterators[index].start()

    for index in xrange(number_threaded_iterators):
        threaded_iterators[index].join()

    return X

def gauss_jacobi_method(graph, min_quadratic_error):

    nodes_list = graph.nodes()
    X_vector = numpy.empty((len(graph.nodes()), 1))
    X_vector.fill(1.0/len(graph.nodes()))
    X_last = numpy.asmatrix(X_vector)

    X = gauss_jacobi_iterate_threaded(graph, nodes_list,  X_last)
    input("Press enter to continue...")
    counter = 1
    while(numpy.linealg.norm(X - X_last) > min_quadratic_error):
        print "Entered Iteration " + str(counter)
        X_last = X
        X = gauss_jacobi_iterate_threaded(graph, nodes_list, X_last)
        input("Press enter to continue...")
        print "Finished Iteration " + str(counter)
        counter += 1

    gauss_jacobi_scores = dict()
    for index in xrange(X.shape[0]):
        gauss_jacobi_scores[index] = {'user_id': nodes_list[index], 'score': X[index, 0]}

    return gauss_jacobi_scores


def main():
    parser = argparse.ArgumentParser(description='Run Gauss-Jacobi threaded algorithm to discover graph centrality')
    parser.add_argument("--input_file", dest="input_file")
    parser.add_argument("--output_file", dest="output_file")
    parser.add_argument("--min_error", dest="min_quadratic_error")
    args = parser.parse_args()

    print "Loading graph"
    graph = nx.read_gpickle(args.input_file)
    print "Loaded graph"
    score_dict = gauss_jacobi_method(graph, float(args.min_quadratic_error))
    with open(args.output_file) as out_file:
        for item in sorted(score_dict.items(), key=lambda (k,v): v['score'], reverse=True):
            out_file.write(str(item[0]) + ' ' + item[1]['user_id'] + ' ' + str(item[1]['score']) + '\n')

if __name__ == '__main__':
    main()