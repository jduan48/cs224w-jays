#!/usr/bin/env python
import json
from sys import argv

DEFAULT_FILE = "DEFAULT_MODEL"
NUMBERS = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]

DATA_FOLDER = "medium-bipartite"
PROFILE_FILE = "json_profile_data"
EDGE_FILE = "json_convo_data"
EDGE_TRAIN_FILE = "json_convo_data_train"
EDGE_TEST_FILE = "json_convo_data_test"
THETA_FILE = "tmp/theta"

RESULT_FOLDER = "result"
PREDICTION_FILE = "prediction"
CORRECT_FILE = "correct"

# https://github.com/mledoze/countries
COUNTRY_FILE = "countries.json"

LOUD = False

def importCountries():
    with open(COUNTRY_FILE, "r") as f:
        countries_list = json.load(f)
        countries = dict([(item["name"], item) for item in countries_list])
    return countries

def importModule():
    if len(argv) == 1:
        with open(DEFAULT_FILE, "r") as f:
            model_name = f.read().strip()
    else:
        model_name = argv[1]
        if model_name.endswith(".py"):
          model_name = model_name[:-len(".py")]
    if LOUD:
        print "Imported model", model_name
    return __import__(model_name)

def importJSON(filename):
    profiles, count = [], 0
    with open(filename, "r") as f:
        for line in f.readlines():
            profiles.append(json.loads(line))
            count += 1
            if LOUD and (count in NUMBERS or count % 5000 == 0):
                print "Imported", count
    return profiles

def importProfile():
    return importJSON(DATA_FOLDER + "/" + PROFILE_FILE)

def importMappedProfiles():
    return dict([(item["id"], item) for item in importProfile()])

def importConvosTrain():
    return importJSON(DATA_FOLDER + "/" + EDGE_TRAIN_FILE)

def importConvosTest():
    return importJSON(DATA_FOLDER + "/" + EDGE_TEST_FILE)

def importConvos():
    return importJSON(DATA_FOLDER + "/" + EDGE_FILE)

def importTheta():
    with open(THETA_FILE, "r") as f:
        theta = json.loads(f.read())
    return theta

def saveTheta(theta):
    with open(THETA_FILE, "w") as f:
        f.write(json.dumps(theta))

def savePrediction(correct, prediction):
    assert len(correct) == len(prediction)
    with open(RESULT_FOLDER + "/" + PREDICTION_FILE, "w") as f:
        f.write("\n".join([str(item) for item in prediction]))
    with open(RESULT_FOLDER + "/" + CORRECT_FILE, "w") as f:
        f.write("\n".join([str(item) for item in correct]))
