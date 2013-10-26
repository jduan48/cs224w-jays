#!/usr/bin/env python

import csv
import json
from random import random

from random_test import train, predict

PROFILE_FILE = "profile"
EDGE_TRAIN_FILE = "edge_input_train"
EDGE_TEST_FILE = "edge_input_test"
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
