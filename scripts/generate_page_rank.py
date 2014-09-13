import networkx as nx
import argparse
import pickle
import re

def load_graph(filename):
    graph = nx.read_gpickle(filename)
    return graph 

def generate_page_rank(graph):
    page_rank_dict = nx.pagerank(graph)
    return page_rank_dict

def output_results(rank_dict, out_filename, cluster_filename):

    user_clusters = None
    with open(cluster_filename, "rb") as infile:
        user_clusters = pickle.load(infile)

    with open(out_filename, 'w') as out_file:
        out_file.write('user_cluster,ranking_score\n')
        for cluster_id in sorted(rank_dict, key=rank_dict.get, reverse=True)[:15]:
            wallet_ids = []
            if re.match(r'^\d+$', cluster_id):
                wallet_ids = [item[0] for item in filter(lambda i: i[1]==int(cluster_id), user_clusters.items())]

            out_file.write(cluster_id + ',' + str(wallet_ids) + ','+  str(rank_dict[cluster_id]) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='filename')
    parser.add_argument('--out', dest='outfile')
    parser.add_argument('--cluster', dest='clusterfilename')
    args = parser.parse_args()

    graph = load_graph(args.filename)
    rank_dict  = generate_page_rank(graph)
    
    output_results(rank_dict, args.outfile, args.clusterfilename)

if __name__ == '__main__':
    main()
