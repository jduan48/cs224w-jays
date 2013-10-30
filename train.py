#!/usr/bin/env python

import csv, json, sys
from random import random
from sys import argv

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

def run():
    print "------------------ TRAINING -----------------"
    with open(PROFILE_FILE, "r") as f:
        profiles = [json.loads(line) for line in f.readlines()]
    with open(EDGE_TRAIN_FILE, "r") as f:
        edges = [json.loads(line) for line in f.readlines()]
    theta = model.train(profiles, edges)
    with open(THETA_FILE, "w") as f:
        f.write(json.dumps(theta))

if __name__ == "__main__":
    importModule()
    run()
