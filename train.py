#!/usr/bin/env python

import csv, json, sys
from random import random
from sys import argv
from import_tool import *

model = importModule()

def run():
    print "Start training..."
    profiles = importMappedProfiles()
    print "Read in", len(profiles), "profiles"
    edges = importConvosTrain()
    print "Loading edges finished."
    theta = model.train(profiles, edges)
    print "Training finished."
    saveTheta(theta)

if __name__ == "__main__":
    run()
