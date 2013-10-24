#!/usr/bin/env python

import csv
import json
from random import random

FOLDER = "test-data"
CONV_FILE = "conversations_dataset"
PROF_FILE = "profiles_dataset.csv"

CONV_ATTRS = [dict(index = 0, attr_name = "id", name = "chat", type = "int"),
              dict(index = 1, attr_name = "user1", name = "user", type = "int"),
              dict(index = 2, attr_name = "user2", name = "user", type = "int"),
              dict(index = 3, attr_name = "profile1", name = "profile", type = "int"),
              dict(index = 4, attr_name = "profile2", name = "profile", type = "int"),
              dict(index = 7, attr_name = "disconnect", name = "user", type = "int"),
              dict(index = 8, attr_name = "reported_id", name = "user", type = "int"),
              dict(index = 9, attr_name = "reported_reason", name = "", type = "string"),
              dict(index = 10, attr_name = "lines1", name = "", type = "int"),
              dict(index = 11, attr_name = "lines2", name = "", type = "int")]

class preJays:

    @staticmethod
    def parseConversation(line):
        items = line.split(";")
        d = dict()
        for attr in CONV_ATTRS:
            d[attr["attr_name"]] = preJays.getData(items[attr["index"]], attr["name"], attr["type"])
        return d

    @staticmethod
    def getData(string, attr_name, type):
        if string in ["null", "0", "{}"]:
            return None
        if attr_name:
            assert string.startswith(attr_name), \
                    "the string doesn't start with the attribute name " + string
            assert string[len(attr_name)] == ":"
            string = string[len(attr_name) + 1:]
        return int(string) if type == "int" else string

    @staticmethod
    def readConversations():
        with open(FOLDER + "/" + CONV_FILE, "r") as f:
            return [preJays.parseConversation(line) for line in f.readlines() if not line.startswith("#")]

if __name__ == "__main__":
    out = preJays.readConversations()
    print json.dumps(out, indent = 4)
