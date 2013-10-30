#!/usr/bin/env python

import csv
import json

from train_mle import train, predict

PROFILE_FILE = "input-data/json_profile_data"
EDGE_TRAIN_FILE = "input-data/json_convo_data_train"
EDGE_TEST_FILE = "input-data/json_convo_data_test"
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
    edges_prediction = predict(profiles, edges_filtered, theta)
    assert len(edges) == len(edges_prediction), "There are " + len(edges) + "edges " +\
            "but only " + len(edges_prediction) + " predictions."
    diff = [edges[i]["lines1"] if edges[i]["lines1"] else 0 +\
            edges[i]["lines2"] if edges[i]["lines2"] else 0 +\
            - edges_prediction[i] for i in range(len(edges))]
    error = (float(sum([x * x for x in diff])) / len(diff)) ** 0.5
    print "the error is", error

if __name__ == "__main__":
    run()




