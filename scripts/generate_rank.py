import networkx as nx
import simplejson as json
import argparse
import pickle
import re

def load_graph(filename):
    graph = nx.read_gpickle(filename)
    return graph 

def generate_page_rank(graph):
    page_rank_dict = nx.pagerank(graph)
    return page_rank_dict

def generate_betweenness_rank(graph):
    betweenness_rank_dict = nx.betweenness_centrality(graph)
    return betweenness_rank_dict

def generate_closeness_rank(graph):
    closeness_rank_dict = nx.closeness_centrality(graph)
    return closeness_rank_dict

def output_results(rank_dict, out_filename, cluster_filename, tag_filename, amount_tops):

    tag_list = None
    with open(tag_filename) as tag_file:
        tag_list_str = ''
        for line in tag_file:
            tag_list_str += line

        tag_list = json.loads(tag_list_str)

    user_clusters = None
    with open(cluster_filename, "rb") as cluster_file:
        user_clusters = pickle.load(cluster_file)

    with open(out_filename, 'w') as out_file:
        out_file.write('user_cluster, wallets_addresses, tags_list, ranking_score\n')
        for cluster_id in sorted(rank_dict, key=rank_dict.get, reverse=True)[:amount_tops]:
            wallet_ids = []
            filtered_tag_str = ''

            if re.match(r'^\d+$', cluster_id):
                wallet_ids = [item[0] for item in filter(lambda i: i[1]==int(cluster_id), user_clusters.items())]
                for wallet_id in wallet_ids:
                    possible_tags = filter(lambda entry: entry['address'] == wallet_id, tag_list)
                    if possible_tags:
                        filtered_tag_str += json.dumps(possible_tags[0]) + ','

            else:
                possible_tags = filter(lambda entry: entry['address'] == cluster_id, tag_list)
                if possible_tags:
                    filtered_tag_str += json.dumps(possible_tags[0]) + ','


            out_file.write(cluster_id + ',' + str(wallet_ids) + ',' + '[' + filtered_tag_str.strip(',') + ']' + ',' +
                           str(rank_dict[cluster_id]) + '\n')

def load_gauss_jacobi_dict(filename):
    gauss_jacobi_dict = dict()
    with open(filename) as file:
        for line in filename:
            parsed_line = line.strip().split()
            user_id, score = parsed_line[1], float(parsed_line[2])
        gauss_jacobi_dict[user_id] = score

    return gauss_jacobi_dict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='filename')
    parser.add_argument('--out', dest='outfile')
    parser.add_argument('--cluster', dest='clusterfilename')
    parser.add_argument('--tag', dest='tagfilename')
    parser.add_argument('--rank_metric', dest='rankmetric')
    parser.add_argument('--size_rank', dest='sizerank')
    args = parser.parse_args()

    if args.rankmetric != "gauss-jacobi":
        graph = load_graph(args.filename)

    rank_dict = None
    if args.rankmetric == 'pagerank':
        rank_dict  = generate_page_rank(graph)
    elif args.rankmetric == 'betweenness':
        rank_dict = generate_betweenness_rank(graph)
    elif args.rankmetric == 'closeness':
        rank_dict = generate_closeness_rank(graph)

    elif args.rankmetric == "gauss-jacobi":
        rank_dict = load_gauss_jacobi_dict(args.filename)
    
    output_results(rank_dict, args.outfile, args.clusterfilename, args.tagfilename, int(args.sizerank))

if __name__ == '__main__':
    main()
