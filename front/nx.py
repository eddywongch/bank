import streamlit as st

from pyvis.network import Network
import networkx as nx

nx_graph = nx.cycle_graph(10)
nx_graph.nodes[1]['title'] = 'Number 1'
nx_graph.nodes[1]['group'] = 1
nx_graph.nodes[3]['title'] = 'I belong to a different group!'
nx_graph.nodes[3]['group'] = 10

nx_graph.add_node(20, size=20, label='Edgar', title='Guanajuato', group=2)
nx_graph.add_node(21, size=15, label='Noe', title='Guanajuato', group=2)
nx_graph.add_edge(20, 21, weight=5)

nx_graph.add_node(25, size=25, label='Eddy', title='DataStax', group=3)
nx_graph.add_node(26, size=25, label='Jason', title='DataStax', group=3)
nx_graph.add_edge(25, 26, weight=5)

nt = Network("500px", "500px")
# populates the nodes and edges data structures
nt.from_nx(nx_graph)
nt.show("nx.html")
