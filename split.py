#!/usr/bin/env python

from random import random
from import_tool import *

PROB_IN_TEST = 0.05

def run():
    with open(DATA_FOLDER + "/" + EDGE_FILE, "r") as f:
        train_file = open(DATA_FOLDER + "/" + EDGE_TRAIN_FILE, "w")
        test_file = open(DATA_FOLDER + "/" + EDGE_TEST_FILE, "w")
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
