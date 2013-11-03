#!/usr/bin/env python

import csv
import json
import os
from sys import argv, path

PROFILE_FILE = "input-data/json_profile_data"
EDGE_TRAIN_FILE = "input-data/json_convo_data_train"
EDGE_TEST_FILE = "input-data/json_convo_data_test"
THETA_FILE = "tmp/theta"
DEFAULT_FILE = "DEFAULT_MODEL"

def importModule():
    global model
    if len(argv) == 1:
        with open(DEFAULT_FILE, "r") as f:
            model_name = f.read().strip()
    else:
        model_name = argv[1]
        if model_name.endswith(".py"):
          model_name = model_name[:-len(".py")]
    model = __import__(model_name)

def computeError(min_length, edges_correct, edges_prediction):
    indices = [i for i in range(len(edges_correct)) if edges_correct[i] >= min_length]
    diff = [edges_prediction[i] - edges_correct[i] for i in indices]
    error = (float(sum([x * x for x in diff])) / len(diff)) ** 0.5
    return (len(indices), error)

def run():
    print "------------------ TESTING -----------------"
    with open(PROFILE_FILE, "r") as f:
        profiles = [json.loads(line) for line in f.readlines()]
        print "Read in", len(profiles), "profiles"
    with open(EDGE_TEST_FILE, "r") as f:
        edges = [json.loads(line) for line in f.readlines()]
        edges_filtered = [(item["user1"], item["user2"]) for item in edges]
        edges_correct = [edges[i]["lines1"] if edges[i]["lines1"] else 0 +\
                         edges[i]["lines2"] if edges[i]["lines2"] else 0 \
                         for i in range(len(edges))]
        print "Read in", len(edges), "edges to predict"
    with open(THETA_FILE, "r") as f:
        theta = json.loads(f.read())
    edges_prediction = model.predict(profiles, edges_filtered, theta)
    assert len(edges) == len(edges_prediction), "There are " + len(edges) + "edges " +\
            "but only " + len(edges_prediction) + " predictions."
    for min_length in [0, 3, 10]:
        num_edges, error = computeError(min_length, edges_correct, edges_prediction)
        print "the error for min length", min_length, "(a total of",\
                num_edges, "conversations) is", error

if __name__ == "__main__":
    importModule()
    run()




