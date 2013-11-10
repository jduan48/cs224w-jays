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

def offByPercentage(edges_correct, edges_prediction, max_diff, min_length):
    indices = [i for i in range(len(edges_correct)) if edges_correct[i] >= min_length]
    return float(sum([1 for i in indices
            if abs(edges_correct[i] - edges_prediction[i]) < max_diff])) / len(indices)

def run():
    print "Start testing..."
    print "Loading profiles..."
    profiles = importProfile()
    print "Read in", len(profiles), "profiles"
    print "Loading convos..."
    edges = importConvosTest()
    edges_filtered = [(item["user1"], item["user2"], item["profile1"], item["profile2"]) for item in edges]
    edges_correct = [edges[i]["lines1"] if edges[i]["lines1"] else 0 +\
                     edges[i]["lines2"] if edges[i]["lines2"] else 0 \
                     for i in range(len(edges))]
    print "Read in", len(edges), "edges to predict"
    print "Loading theta..."
    theta = importTheta()
    print "Theta loaded..."
    print "Predicting..."
    edges_prediction = model.predict(profiles, edges_filtered, theta)
    savePrediction(edges_correct, edges_prediction)
    assert len(edges) == len(edges_prediction), "There are " + len(edges) + "edges " +\
            "but only " + len(edges_prediction) + " predictions."
    for min_length in [0, 1, 3, 10]:
        print "Min length", min_length
        print "Off by", " ".join([str(max_diff) + ":" + str(offByPercentage(edges_correct, edges_prediction, max_diff, min_length)) + " " for max_diff in [1, 2, 3, 4, 5]])

if __name__ == "__main__":
    run()
