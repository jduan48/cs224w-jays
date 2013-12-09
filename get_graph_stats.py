#!/usr/bin/env python

from itertools import combinations_with_replacement
import networkx as nx
import csv, json, sys
from random import random
from random import sample
from operator import itemgetter
from sys import argv
from import_tool import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict

IS_BIPARTITE = False
PLOTS_FOLDER = "plots"
DEGREE_DISTRIBUTION_FILE = "degree_distribution.png"
REDUNDANCY_DISTRIBUTION_FILE = "redundancy_distribution.png"
THRESH = 10

def createGraph(convos):
    graph1 = nx.Graph()
    graph2 = nx.Graph()
    for convo in convos:
        length = convo["lines1"] if convo["lines1"] else 0 + convo["lines2"] if convo["lines2"] else 0
        profile1 = convo["profile1"]
        profile2 = convo["profile2"]
<<<<<<< HEAD
        if length > 0:
            if not graph1.has_node(profile1):
                graph1.add_node(profile1)
            if not graph1.has_node(profile2):
                graph1.add_node(profile2)
            graph1.add_edge(profile1, profile2)
        if not graph2.has_node(profile1):
            graph2.add_node(profile1)
        if not graph2.has_node(profile2):
            graph2.add_node(profile2)
        graph2.add_edge(profile1, profile2)
    return (graph1, graph2)
=======
        if not graph.has_node(profile1):
            graph.add_node(profile1)
        if not graph.has_node(profile2):
            graph.add_node(profile2)
        l1 = convo["lines1"] if convo["lines1"] else 0
        l2 = convo["lines2"] if convo["lines2"] else 0
        graph.add_edge(profile1, profile2,
                       success=(l1 + l2 >= THRESH))
    return graph
>>>>>>> 46a918b0fd6c81b884539e3fe3d86ab30420868d

def get_node_sets(graph):
    if not IS_BIPARTITE:
        return (None, None)
    coloring = nx.bipartite.color(graph)
    X = set()
    Y = set()
    for key, value in coloring.iteritems():
        if value:
            X.add(key)
        else:
            Y.add(key)
    return (X, Y)

def drawHistogram(values, filename, bar_width, xlabel, ylabel):
    drawStacked(values, None, filename, bar_width, xlabel, ylabel)

def get_xy(values):    
    histogram = defaultdict(int)
    for value in values:
        histogram[value] += 1
    x_vals = histogram.keys()
    x_vals.sort()
    y_vals = [histogram[x] for x in x_vals]
    return x_vals, y_vals
    
def drawStacked(v1, v2, filename, bar_width, xlabel, ylabel):
    plt.clf()
    x1, y1 = get_xy(v1)
    plt.bar(x1, y1, width=bar_width, color='b')
    if v2: # not tested
        x2, y2 = get_xy(v2)
        plt.bar(x2, y2, width=bar_width, color='r', bottom=y1)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.savefig('/'.join([PLOTS_FOLDER, filename]))


"""
Returns number of nodes in each connected component and its diameter.
"""
def get_diameters(graph):
    connected_components = nx.connected_component_subgraphs(graph)
    print "number of connected components: ", len(connected_components)
    diameters = []
    for subgraph in connected_components:
        diameters.append((len(subgraph), nx.diameter(subgraph)))
    print "diameters: ", diameters

def get_clustering(graph):
    #print "clustering: ", nx.bipartite.clustering(graph)
    if IS_BIPARTITE:
        print "average clustering: ", nx.bipartite.average_clustering(graph)
    else:
        print "average clustering: ", nx.average_clustering(graph)

def get_density(graph, X):
    if IS_BIPARTITE:
        print "density: ", nx.bipartite.density(graph, X)

def get_degree_distribution(graph):
    degrees = list(graph.degree(graph.nodes()).values())
    drawHistogram(degrees, DEGREE_DISTRIBUTION_FILE, 1, "Degree", "Frequency")

def get_node_redundancy(graph):
    if not IS_BIPARTITE:
        return
    redundancies = nx.bipartite.node_redundancy(graph)
    redundancies = map(lambda x: round(x, 1), redundancies.values())
    drawHistogram(redundancies, REDUNDANCY_DISTRIBUTION_FILE, 0.1, "Node Redundancy", "Frequency")

def render_graph(graph):
    plt.clf()
    nx.draw(graph)
    plt.savefig('/'.join([PLOTS_FOLDER, "layout.png"]))

def get_success_distribution(graph):
    pairs = []
    for node in sample(nx.nodes(graph), 200):
        vals = [graph.edge[node][neigh]["success"] for neigh in nx.all_neighbors(graph, node)]
        t = vals.count(True)
        pairs.append([t, len(vals) - t])
    pairs.sort(key = itemgetter(0, 1), reverse=True)
    x = range(len(pairs))
    y1 = [val[0] for val in pairs]
    y2 = [val[1] for val in pairs]
    plt.clf()
    plt.bar(x, y1, color='b')
    plt.bar(x, y2, color='r', bottom=y1)
    plt.savefig("plots/success_hist.png")

def run():
    edges = importConvosTrain()
    (convo_graph, full_graph) = createGraph(edges)
    print "full graph edges: ", len(full_graph.edges())
    print "full graph nodes: ", len(full_graph.nodes()) 
    print "convo graph edges: ", len(convo_graph.edges())
    print "convo graph nodes: ", len(convo_graph.nodes())   
    # render_graph(full_graph)
    get_success_distribution(full_graph)
    X, Y = get_node_sets(convo_graph)

    get_diameters(convo_graph)
    get_clustering(convo_graph)
    get_density(convo_graph, X)
    get_degree_distribution(convo_graph)
    get_node_redundancy(convo_graph)

if __name__ == "__main__":
    run()
