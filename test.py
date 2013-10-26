#!/usr/bin/env python

import csv
import json

from random_test import train, predict

PROFILE_FILE = "profile"
EDGE_TRAIN_FILE = "edge_input_train"
EDGE_TEST_FILE = "edge_input_test"
THETA_FILE = "tmp/theta"

def run():
    print "------------------ TESTING -----------------"
    with open(PROFILE_FILE, "r") as f:
        profiles = [json.loads(line) for line in f.readlines()]
        print "Read in", len(profiles), "profiles"
    with open(EDGE_TEST_FILE, "r") as f:
        edges = [json.loads(line) for line in f.readlines()]
        edges_filtered = [(item["user1"], item["user2"]) for item in edges]
        print "Read in", len(edges), "edges to predict"
    with open(THETA_FILE, "r") as f:
        theta = json.loads(f.read())
    edge_prediction = predict(profiles, edges_filtered, theta)
    assert len(edges) == len(edges_prediction), "There are " + len(edges) + "edges " +\
            "but only " + len(edges_prediction) + " predictions."
    diff = [edges[i]["lines1"] + edges[i]["lines2"] - edges_prediction[i] for i in range(len(edges))]
    error = sum([x * x for x in diff])
    print "the error is", error

if __name__ == "__main__":
    run()




