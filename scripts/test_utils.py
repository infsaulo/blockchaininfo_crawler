import pytest
from utils import calculate_precision, calculate_average_precision
from pagerank import PageRank
from graph_scripts import get_major_strongly_component

from networkx import DiGraph
import networkx as nx

class TestUtils:
    relevant_entries = [1,2,4,6,8,9,10]
    retrieved_entries = [1,2,4,8,9,13,6]
    graph = DiGraph()
    graph.add_edge(1,2)
    graph.add_edge(2,1)
    graph.add_edge(1,4)
    graph.add_edge(1,3)
    graph.add_edge(2,4)
    graph.add_edge(4,2)
    graph.add_edge(4,3)
    graph.add_edge(4,1)

    def test_calculate_precision(self):
        precision_value = calculate_precision(self.relevant_entries, self.retrieved_entries)
        assert precision_value >= 0.85 and precision_value <= 0.858

    def test_calculate_average_precision(self):
        average_precision = calculate_average_precision(self.relevant_entries, self.retrieved_entries)
        assert average_precision >= 0.89 and average_precision <= 0.892

    def test_calculate_page_rank(self):

        pagerank = PageRank(self.graph, 0.85, 0.0001)
        pagerank_dict = pagerank.run()

        for k, v in pagerank_dict.items():
            print k, v

        assert True

    def test_strongly_connected_component(self):
        subgraph = get_major_strongly_component(self.graph)

        list_len = []
        for component in nx.strongly_connected_components(self.graph):
            list_len.append(len(component))

        assert len(subgraph.nodes()) == sorted(list_len)[-1]
