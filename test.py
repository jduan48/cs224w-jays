#!/usr/bin/env python

import csv
import json
import os
from sys import argv, path
from import_tool import *

model = importModule()

def computeError(min_length, edges_correct, edges_prediction):
    indices = [i for i in range(len(edges_correct)) if edges_correct[i] >= min_length]
    diff = [edges_prediction[i] - edges_correct[i] for i in indices]
    error = (float(sum([x * x for x in diff])) / len(diff)) ** 0.5
    return (len(indices), error)

def run():
    print "Start testing..."
    print "Loading profiles..."
    profiles = importProfile()
    print "Read in", len(profiles), "profiles"
    print "Loading convos..."
    edges = importConvos()
    edges_filtered = [(item["user1"], item["user2"]) for item in edges]
    edges_correct = [edges[i]["lines1"] if edges[i]["lines1"] else 0 +\
                     edges[i]["lines2"] if edges[i]["lines2"] else 0 \
                     for i in range(len(edges))]
    print "Read in", len(edges), "edges to predict"
    print "Loading theta..."
    theta = importTheta()
    print "Theta loaded..."
    print "Predicting..."
    edges_prediction = model.predict(profiles, edges_filtered, theta)
    assert len(edges) == len(edges_prediction), "There are " + len(edges) + "edges " +\
            "but only " + len(edges_prediction) + " predictions."
    for min_length in [0, 3, 10]:
        num_edges, error = computeError(min_length, edges_correct, edges_prediction)
        print "the error for min length", min_length, "(a total of",\
                num_edges, "conversations) is", error

if __name__ == "__main__":
    run()
