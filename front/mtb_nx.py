#!/usr/bin/python3

from cassandra.cluster import Cluster, EXEC_PROFILE_GRAPH_DEFAULT
from cassandra.datastax.graph import GraphProtocol
from cassandra.datastax.graph.fluent import DseGraph

import networkx as nx

import streamlit as st
from pyvis.network import Network

class DseLoader:
    def __init__(self, name):
        self.name = name

    def initialize(self):
         print("Initialize")

    def connect(self, ip, keyspace):
         # Not blank
        if ip and ip.strip():
            self.ip = ip
        else:
            self.ip = '10.101.33.239' # default

        # Create an execution profile, using GraphSON3 for Core graphs
        self.ep = DseGraph.create_execution_profile(
            keyspace,
            graph_protocol=GraphProtocol.GRAPHSON_3_0)

        self.cluster = Cluster(execution_profiles={EXEC_PROFILE_GRAPH_DEFAULT: self.ep}, contact_points=[self.ip])
        self.session = self.cluster.connect()

        self.g = DseGraph.traversal_source(session=self.session)


    def traverse(self):
        g = self.g

        #traversal1 = g.V().has('person', 'name', 'Chet Kapoor').next()
    

        #for v in verts:
        #    print(v)

        #for e in g.E():
        #    print(e)

        # Vertices
        verts = g.V()
        for v in verts:
            print("***", v.id )
            
            #for p in g.V(v).properties():
                #name = p.properties('name').value()
            #    print("key:",p.label, "| value: " ,p.value)

        # Edges
        edges = g.E()
        for e in edges:
            print("***", e.id, '\n' , DseLoader.parseEdgeId(e.id) )
            
            #for p in g.E(e).properties():
            #    print("key:",e.label, "| value: " ,e.value)

        print("**** end traverse")

        return g

    ##################################################################
    # DSE Graph 6.8.x encodes vertex and edge ids in a particular way
    # 

    #############################################
    # Parses a DSE edge id string into its components
    # Example:
    # dseg:/person-mentioned-quote/bf720fd3069c1704fd25359e1ebb77e531c4949a/069ae73d2bc4f54419a6c3fc56a0723c1b041740
    # Returns:
    # A dict with the following:
    # source_label: person
    # dest_label: quote
    # edge_label: mentioned
    # source_id: bf720fd3069c1704fd25359e1ebb77e531c4949a
    # dest_id: 069ae73d2bc4f54419a6c3fc56a0723c1b041740

    def parseEdgeId(str):
        result = {}

        str_list = str.split('/')
        edge_str = str_list[1]
        edge_list = edge_str.split('-')
        
        result['source_label'] = edge_list[0]
        result['dest_label'] = edge_list[2]
        result['edge_label'] = edge_list[1]
        result['source_id'] = str_list[2]
        result['dest_id'] = str_list[4]

        return result

    #############################################
    # Parses a DSE vertex id string into its components
    # Example:
    # dseg:/person/bf720fd3069c1704fd25359e1ebb77e531c4949a
    # Returns:
    # A dict with the following:
    # vertex_label: person
    # vertex_id: bf720fd3069c1704fd25359e1ebb77e531c4949a


    def parseVertexId(str):
        result = {}

        str_list = str.split('/')    
        result['vertex_label'] = str_list[1]
        result['vertex_id'] = str_list[2]
    

        return result

    ####################################
    # Convert Gremlin graph to Nx graph
    # returns a Networkx graph
    ####################################
   
    def convertG2Nx(g):
        # Creating NetworkX graph
        GG = nx.MultiGraph()
        
        # Edges
        edges = g.E()
        props = []
        for e in edges:
            es = DseLoader.parseEdgeId(e.id)
            print("*** Edges", e.id , es)
            #print("*** Edges Props: ", e)
            trans_str = "transaction: " + es['source_id'] + ":" + es['dest_id']
            
            # Processing edge properties
            for p in g.E(e).properties():
                #print("Properties:", p)
                #print("key:",p.key, "| value: " ,p.value)
                props.append({ p.key : p.value})

            print("Properties: ", props)

            '''

            initial_props = [ {'edge_label' : es['edge_label'] }, \
                        {'source_label' : es['source_label']}, {'dest_label': es['dest_label']}, {'label' : trans_str} ]
            initial_props.append(props)

            #edge_props = [ es['source_id'], es['dest_id'] ]
            #edge_props.append(initial_props)
            '''

            GG.add_edge(es['source_id'], es['dest_id'], edge_label=es['edge_label'], \
                       source_label=es['source_label'], dest_label=es['dest_label'], label = trans_str)
           

        # Vertices
        verts = g.V()
        for v in verts:
            vp = DseLoader.parseVertexId(v.id)
            print("*** Verts", v.id , vp)
            id = vp['vertex_id']


            for p in g.V(v).properties():
                print("Properties: ", p)
                print("key:",p.label, "| value: " ,p.value)
                
                # Adding property to the vertex
                if p.label == 'contactFirstName':
                    GG.add_node(id, label= p.value, attr1 = 'bla', attr2= 'bla2')
                #else:
                #    GG.add_nodes_from([(id, {p.label: p.value}),])
		
            #attrs = {id: {"attr1": 20, "attr2": "nothing"}}
            #nx.set_node_attributes(GG, attrs)

		#nx_graph.add_node(20, size=20, label='Edgar', title='Guanajuato', group=2)
		#nx_graph.add_node(21, size=15, label='Noe', title='Guanajuato', group=2)

        for v in GG.nodes():
            print("*** Nodes" , v)
            attrs = {v: {"attr1": 20, "attr2": "nothing"}}
            nx.set_node_attributes(GG, attrs)
            print(nx.get_node_attributes(GG, v))

        return GG



dl = DseLoader("loader")         # Constructor
dl.initialize()                 # Init
dl.connect('10.101.33.239','mtb')     # Connect
g = dl.traverse()

# Convert dse to nx
gg = DseLoader.convertG2Nx(g)

# Setting attibutes
lbls = nx.get_node_attributes(gg, 'attr2') 
#nx.draw(gg,labels=lbls,node_size=100)
pos = nx.spring_layout(gg)
nx.draw_networkx_labels(gg, pos, labels = lbls)
nx.draw(gg, with_labels = True)

nt = Network("500px", "900px")
# populates the nodes and edges data structures
nt.from_nx(gg)
#nt.show_buttons(filter_=['physics'])


nt.show("mtb_nx.html") 

