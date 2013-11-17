#!/usr/bin/env python

import csv
import json
import os
from sys import argv, path
from import_tool import *

model = importModule()

thresholds = [1, 3]

def computeError(min_length, edges_correct, edges_prediction):
    indices = [i for i in range(len(edges_correct)) if edges_correct[i] >= min_length]
    diff = [edges_prediction[i] - edges_correct[i] for i in indices]
    error = (float(sum([x * x for x in diff])) / len(diff)) ** 0.5
    return (len(indices), error)

def offByPercentage(edges_correct, edges_prediction, max_diff, min_length):
    indices = [i for i in range(len(edges_correct)) if edges_correct[i] >= min_length]
    return float(sum([1 for i in indices
            if abs(edges_correct[i] - edges_prediction[i]) < max_diff])) / len(indices)

def positiveNegative(edges_correct, edges_prediction, threshold):
    counts = [0,] * 4
    for i in range(len(edges_correct)):
        counts[int(edges_correct[i] >= threshold) * 2 + int(edges_prediction[i] >= threshold)] += 1
    return map(lambda x: x / float(len(edges_correct)), counts)

def run():
    print "Start testing..."
    profiles = importMappedProfiles()
    print "Read in", len(profiles), "profiles"
    edges = importConvosTest()
    edges_filtered = [(item["user1"], item["user2"], item["profile1"], item["profile2"]) for item in edges]
    edges_correct = [edges[i]["lines1"] if edges[i]["lines1"] else 0 +\
                     edges[i]["lines2"] if edges[i]["lines2"] else 0 \
                     for i in range(len(edges))]
    print "Read in", len(edges), "edges to predict"
    theta = importTheta()
    print "Theta loaded..."
    edges_prediction = model.predict(profiles, edges_filtered, theta)
    savePrediction(edges_correct, edges_prediction)
    assert len(edges) == len(edges_prediction), "There are " + len(edges) + "edges " +\
            "but only " + len(edges_prediction) + " predictions."
    for threshold in thresholds:
        percentages = positiveNegative(edges_correct, edges_prediction, threshold)
        print "Threshold: %s \t At least \t\t Less than \t (Actual)" % threshold
        print "At least \t %s \t %s" % (percentages[3], percentages[1])
        print "Less than \t %s \t %s\n" % (percentages[2], percentages[0])

if __name__ == "__main__":
    run()
