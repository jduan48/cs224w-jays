#!/usr/bin/env python

from import_tool import importJSON, importMappedProfiles
import verify_consistency
import json
import sys

g = "gender"
rep = "reported_id"
disc = "disconnected_id"

def valid(profiles, edge):
    p1 = edge["profile1"]
    p2 = edge["profile2"]
    if profiles[p1][g] == None or profiles[p2][g] == None or \
       profiles[p1][g] == profiles[p2][g]:
        return False
    if profiles[p1][g] == "F":
        edge["profile1"], edge["profile2"] = p2, p1
        edge["user1"], edge["user2"] = edge["user2"], edge["user1"]
        edge["lines1"], edge["lines2"] = edge["lines2"], edge["lines1"]
        swap = {
            edge["user2"] : edge["user1"],
            edge["user1"] : edge["user2"],
            None : None,
        }
        edge["reported_id"] = swap[edge["reported_id"]]
        edge["disconnect"] = swap[edge["disconnect"]]
    upmap = {
        edge["user1"] : edge["profile1"],
        edge["user2"] : edge["profile2"],
        None : None,
    }
    edge["reported_id"] = upmap[edge["reported_id"]]
    edge["disconnect"] = upmap[edge["disconnect"]]
    return True

def run(convoFile):
    profiles = importMappedProfiles()
    edges = importJSON(convoFile)
    verify_consistency.run(edges)

    with open(convoFile + "_bipartite", "w") as outfile:
        for edge in edges:
            if valid(profiles, edge):
                json.dump(edge, outfile)
                outfile.write('\n')

if __name__ == "__main__":
    run(sys.argv[1])
