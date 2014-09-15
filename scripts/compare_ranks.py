import re
import argparse
import simplejson as json

from utils import calculate_average_precision, calculate_kendalltau

def parse_file(filename):
    list_ids = []
    with open(filename) as ranking_file:
        for line in ranking_file:
            list_ids.append(re.search(r'^([^,]+),', line).group(1).strip())

    return list_ids

def compare_ranks(rank1, rank2):
    kendall_metric = calculate_kendalltau(rank1, rank2)

    return kendall_metric

def output_results(result_list, outfilename):
    with open(outfilename, 'w') as outfile:
        for result in result_list:
            outfile.write(json.dumps(result) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--listfiles', dest='listfilenames')
    parser.add_argument('--out', dest='outfile')
    parser.add_argument('--comparison_method', dest='method')
    args = parser.parse_args()

    list_of_files = map(lambda filename: {'filename' : filename}, args.listfilenames.split(','))
    for index in xrange(len(list_of_files)):
        list_of_files[index]['ranking'] = parse_file(list_of_files[index]['filename'])

    list_ranking_comparisons = []
    for index in xrange(len(list_of_files)-1):
        comparison_result = {'file1': list_of_files[index]['filename'], 'file2': list_of_files[index+1]['filename']}
        if args.method == 'kendall':
            comparison_result['result'] = calculate_kendalltau(list_of_files[index]['ranking'],
                                                               list_of_files[index+1]['ranking'])
        elif args.method == 'sets':
            comparison_result['result'] = calculate_average_precision(list_of_files[index]['ranking'],
                                                                      list_of_files[index+1]['ranking'])
        list_ranking_comparisons.append(comparison_result)

    output_results(list_ranking_comparisons, args.outfile)


if __name__ == '__main__':
    main()