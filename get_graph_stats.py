#!/usr/bin/env python

from itertools import combinations_with_replacement
import networkx as nx
import csv, json, sys
from random import random
from sys import argv
from import_tool import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict

PLOTS_FOLDER = "plots"
DEGREE_DISTRIBUTION_FILE = "degree_distribution.png"
REDUNDANCY_DISTRIBUTION_FILE = "redundancy_distribution.png"

def createGraph(convos):
    graph = nx.Graph()
    for convo in convos:
        profile1 = convo["profile1"]
        profile2 = convo["profile2"]
        if not graph.has_node(profile1):
            graph.add_node(profile1)
        if not graph.has_node(profile2):
            graph.add_node(profile2)
        graph.add_edge(profile1, profile2)
    return graph

def get_node_sets(graph):
    coloring = nx.bipartite.color(graph)
    X = set()
    Y = set()
    for key, value in coloring.iteritems():
        if value:
            X.add(key)
        else:
            Y.add(key)
    return (X, Y)

def drawHistogram(values, filename, bar_width):
    plt.clf()
    histogram = defaultdict(int)
    for value in values:
        histogram[value] += 1
    x_vals = histogram.keys()
    x_vals.sort()
    y_vals = [histogram[x] for x in x_vals]
    plt.bar(x_vals, y_vals, width=bar_width)
    plt.savefig('/'.join([PLOTS_FOLDER, filename]))

"""
Returns number of nodes in each connected component and its diameter.
"""
def get_diameters(graph):
    connected_components = nx.connected_component_subgraphs(graph)
    diameters = []
    for subgraph in connected_components:
        diameters.append((len(subgraph), nx.diameter(subgraph)))
    print "diameters: ", diameters

def get_clustering(graph):
    #print "clustering: ", nx.bipartite.clustering(graph)
    print "average clustering: ", nx.bipartite.average_clustering(graph)

def get_density(graph, X):
    print "density: ", nx.bipartite.density(graph, X)

def get_degree_distribution(graph, X):
    degrees = nx.bipartite.degrees(graph, X)
    drawHistogram(degrees[0].values(), DEGREE_DISTRIBUTION_FILE, 1)

def get_node_redundancy(graph):
    redundancies = nx.bipartite.node_redundancy(graph)
    redundancies = map(lambda x: round(x, 1), redundancies.values())
    drawHistogram(redundancies, REDUNDANCY_DISTRIBUTION_FILE, 0.1)

def run():
    edges = importConvosTrain()
    graph = createGraph(edges)
    X, Y = get_node_sets(graph)

    get_diameters(graph)
    get_clustering(graph)
    get_density(graph, X)
    get_degree_distribution(graph, X)
    get_node_redundancy(graph)
    
if __name__ == "__main__":
    run()
