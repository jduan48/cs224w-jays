#!/usr/bin/env python
import json
from sys import argv

DEFAULT_FILE = "DEFAULT_MODEL"
NUMBERS = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]

PROFILE_FILE = "input-data/json_profile_data"
EDGE_TRAIN_FILE = "input-data/json_convo_data_train"
EDGE_TEST_FILE = "input-data/json_convo_data_test"
THETA_FILE = "tmp/theta"

def importModule():
    if len(argv) == 1:
        with open(DEFAULT_FILE, "r") as f:
            model_name = f.read().strip()
    else:
        model_name = argv[1]
        if model_name.endswith(".py"):
          model_name = model_name[:-len(".py")]
    print "Imported model", model_name
    return __import__(model_name)

def importJSON(filename):
    profiles, count = [], 0
    with open(filename, "r") as f:
        for line in f.readlines():
            profiles.append(json.loads(line))
            count += 1
            if count in NUMBERS or count % 5000 == 0:
                print "Imported", count
    return profiles

def importProfile():
    return importJSON(PROFILE_FILE)

def importConvosTrain():
    return importJSON(EDGE_TRAIN_FILE)

def importConvosTest():
    return importJSON(EDGE_TEST_FILE)

def importTheta():
    with open(THETA_FILE, "r") as f:
        theta = json.loads(f.read())
    return theta

def saveTheta(theta):
    with open(THETA_FILE, "w") as f:
        f.write(json.dumps(theta))
