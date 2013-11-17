#!/usr/bin/env python

from import_tool import importConvos, importMappedProfiles
import profiles

def run(edges):
    profs = importMappedProfiles()
    for edge in edges:
        for u in [edge["profile1"], edge["profile2"]]:
            if int(u) not in profs:
                print u

if __name__ == "__main__":
    run(importConvos())
