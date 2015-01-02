from scipy.sparse import *
import networkx as nx
import argparse
import logging
import numpy
import time
import math

def normalize(A):
    A = A.T
    sum_of_col = A.sum(0).tolist()
    c = []
    for i in sum_of_col:
        for j in i:
            if math.fabs(j) <= 0.0:
                c.append(0)
            else:
                c.append(1/j)
    B = lil_matrix((A.shape[0],A.shape[1]))
    B.setdiag(c)

    C = A*B
    C = C.T
    return C

def main():
    parser = argparse.ArgumentParser(description='Run Gauss-Jacobi threaded algorithm to discover graph centrality')
    parser.add_argument("--input_file", dest="input_file")
    parser.add_argument("--output_file", dest="output_file")
    parser.add_argument("--min_error", dest="min_quadratic_error")
    parser.add_argument("--alpha", dest="alpha_factor")
    args = parser.parse_args()

    print "Loading the graph"
    graph = nx.read_gpickle(args.input_file)
    print "Loaded the graph"
    A = nx.to_scipy_sparse_matrix(graph)
    A = normalize(A).T
    I = identity(A.shape[0])
    A = I - float(args.alpha_factor)*(I - A)
    
    nodes_list = graph.nodes()
    X_vector = numpy.empty((len(graph.nodes()), 1))
    sum_degree = 0
    for node in nodes_list:
        sum_degree += len(graph.predecessors(node))
    for index in xrange(len(nodes_list)):
    	X_vector[index, 0] = float(len(graph.predecessors(nodes_list[index])))/sum_degree
    X_last = numpy.asmatrix(X_vector)
    X = A * X_last
    logging.basicConfig(filename='/mnt/bitcoin/saulomrr/data/log_power_method_bigger.log',level=logging.DEBUG)
    logging.debug(time.strftime("%H:%M:%S") + ' ZERO ITERATION')
    logging.debug(time.strftime("%H:%M:%S") + ' ERROR: %s' % str(numpy.linalg.norm(X - X_last)))
    logging.debug(time.strftime("%H:%M:%S") + 'VECTOR: \n' + '\n'.join([str(X.item(index, 0)) + ' ' + nodes_list[index] for index in xrange(X.shape[0])]))
    counter = 1
    while(numpy.linalg.norm(X - X_last) > float(args.min_quadratic_error)):
        print "Iteration: %s" % str(counter)
        X_last = X
        X = A * X_last
        logging.debug(time.strftime("%H:%M:%S") +  ' %s ITERATION' % str(counter))
        logging.debug(time.strftime("%H:%M:%S") +  ' ERROR: %s' % str(numpy.linalg.norm(X - X_last)))
        logging.debug(time.strftime("%H:%M:%S") + 'VECTOR: \n' + '\n'.join([str(X.item(index, 0)) + ' ' + nodes_list[index] for index in xrange(X.shape[0])]))
        counter += 1

    power_method_scores = dict()
    for index in xrange(X.shape[0]):
        power_method_scores[index] = {'user_id': nodes_list[index], 'score': X[index, 0]}
    
    with open(args.output_file, 'w') as out_file:
        for item in sorted(power_method_scores.items(), key=lambda (k,v): v['score'], reverse=True):
            out_file.write(str(item[0]) + ' ' + item[1]['user_id'] + ' ' + str(item[1]['score']) + '\n')

if __name__ == "__main__":
    main()
