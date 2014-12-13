import networkx as nx
import argparse
import numpy

def get_major_strongly_component(graph):

    major_strongly_component_dict = {'amount_nodes': 0, 'subgraph':None}
    for component in nx.strongly_connected_component_subgraphs(graph):
        amount_nodes = len(component.nodes())
        if amount_nodes > major_strongly_component_dict['amount_nodes']:
            major_strongly_component_dict['amount_nodes'] = amount_nodes
            major_strongly_component_dict['subgraph'] = component

    return major_strongly_component_dict['subgraph']

def output_in_file(object, output_filename):
    nx.write_gpickle(object, output_filename)

def gauss_jacobi_iterate(graph, nodes_list, X_last):
    
    X = numpy.asmatrix(numpy.empty((X_last.shape[0], 1)))
    for index in xrange(X.shape[0]):
        print "Getting k predecessors of " + str(index) 
        list_dict_adjacencies = graph.predecessors(nodes_list[index])
        print "Got k predecessors of " + str(index)
        value = 0.0
        for node in list_dict_adjacencies:
            node_index = nodes_list.index(node)
            value += (1.0/len(list_dict_adjacencies)) * X_last[node_index, 0]
        X[index] = value
    
    return X

def gauss_jacobi_method(graph, min_quadratic_error):
    
    nodes_list = graph.nodes()
    X_vector = numpy.empty((len(graph.nodes()), 1))
    X_vector.fill(1.0/len(graph.nodes()))
    X_last = numpy.asmatrix(X_vector)
    
    X = gauss_jacobi_iterate(graph, nodes_list,  X_last)
    counter = 1
    while(numpy.linealg.norm(X - X_last) > min_quadratic_error):
        print "Entered Iteration " + str(counter)
        X_last = X
        X = gauss_jacobi_iterate(graph, nodes_list, X_last)
        print "Finished Iteration " + str(counter)
        counter += 1

    gauss_jacobi_scores = dict()
    for index in xrange(X.shape[0]):
        gauss_jacobi_scores[index] = {'user_id': nodes_list[index], 'score': X[index, 0]}

    return gauss_jacobi_scores
 
def main():

    parser = argparse.ArgumentParser(description='Generate some metrics and graph-related objects to bitcoin network')
    parser.add_argument("--script", dest="script")
    parser.add_argument("--is_file_put", dest='is_out_file')
    parser.add_argument("--input_file", dest="input_file")
    parser.add_argument("--output_file", dest="output_file")
    parser.add_argument("--min_error", dest="min_quadratic_error")
    args = parser.parse_args()

    print "Loading graph"
    graph = nx.read_gpickle(args.input_file)
    print "Loaded graph"
    if args.script == 'major_strongly_component' :
        subgraph = get_major_strongly_component(graph)
        if bool(args.is_out_file):
            output_in_file(subgraph, args.output_file)
    
    if args.script == 'gauss_jacobi':
        score_dict = gauss_jacobi_method(graph, float(args.min_quadratic_error))
        with open(args.output_file) as out_file:
            for item in sorted(score_dict.items(), key=lambda (k,v): v['score'], reverse=True):
                out.write(str(item[0]) + ' ' + item[1]['user_id'] + ' ' + str(item[1]['score']) + '\n')

if __name__ == '__main__':
    main()
