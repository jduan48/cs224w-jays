#!/usr/bin/env python

from random import random

PROB_IN_TEST = 0.05

EDGE_FILE = "input-data/json_convo_data"
EDGE_TRAIN_FILE = "input-data/json_convo_data_train"
EDGE_TEST_FILE = "input-data/json_convo_data_test"

def run():
    with open(EDGE_FILE, "r") as f:
        train_file = open(EDGE_TRAIN_FILE, "w")
        test_file = open(EDGE_TEST_FILE, "w")
        while True:
            line = f.readline()
            if not line:
                break
            if random() < PROB_IN_TEST:
                test_file.write(line)
            else:
                train_file.write(line)
        train_file.close()
        test_file.close()

if __name__ == "__main__":
    run()
