import networkx as nx
import argparse

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

def main():

    parser = argparse.ArgumentParser(description='Generate some metrics and graph-related objects to bitcoin network')
    parser.add_argument("--script", dest="script")
    parser.add_argument("--is_file_put", dest='is_out_file')
    parser.add_argument("--input_file", dest="input_file")
    parser.add_argument("--output_file", dest="output_file")
    args = parser.parse_args()

    if args.script == 'major_strongly_component':
        graph = nx.read_gpickle(args.input_file)
        subgraph = get_major_strongly_component(graph)
        if bool(args.is_out_file):
            output_in_file(subgraph, args.output_file)

if __name__ == '__main__':
    main()