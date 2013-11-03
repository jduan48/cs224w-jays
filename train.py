#!/usr/bin/env python

import csv, json, sys
from random import random
from sys import argv
from import_tool import *

model = importModule()

def run():
    print "Start training..."
    print "Loading profiles..."
    profiles = importProfile()
    print "Read in", len(profiles), "profiles"
    print "Loading edges..."
    edges = importConvosTrain()
    print "Loading edges finished."
    print "Training..."
    theta = model.train(profiles, edges)
    print "Training finished."
    saveTheta(theta)

if __name__ == "__main__":
    run()
