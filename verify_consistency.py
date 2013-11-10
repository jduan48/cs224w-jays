#!/usr/bin/env python

from import_tool import *
import mappify_profiles

def run():
    profs = mappify_profiles.get_all()
    print "Loading convos..."
    edges = importConvos()
    print "Read in", len(edges), "edges"
    for edge in edges:
        for u in [edge["profile1"], edge["profile2"]]:
            if int(u) not in profs:
                print u

if __name__ == "__main__":
    run()
