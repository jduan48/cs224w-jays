#!/usr/bin/env python

import csv, json, sys
from random import random
from models.train_instance_average import train, predict


PROFILE_FILE = "input-data/json_profile_data"
EDGE_TRAIN_FILE = "input-data/json_convo_data_train"
EDGE_TEST_FILE = "input-data/json_convo_data_test"
THETA_FILE = "tmp/theta"

def run():
    print "------------------ TRAINING -----------------"
    with open(PROFILE_FILE, "r") as f:
        profiles = [json.loads(line) for line in f.readlines()]
    with open(EDGE_TRAIN_FILE, "r") as f:
        edges = [json.loads(line) for line in f.readlines()]
    theta = train(profiles, edges)
    with open(THETA_FILE, "w") as f:
        f.write(json.dumps(theta))

if __name__ == "__main__":
    run()
