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

PROF_ATTRS = [dict(index = 0, attr_name = "id", name = "profile", type = "int"),
              dict(index = 1, attr_name = "location", name = "", type = "string"),
              dict(index = 3, attr_name = "age", name = "", type = "int"),
              dict(index = 4, attr_name = "gender", name = "", type = "string"),
              dict(index = 6, attr_name = "about", name = "", type = "dict")]

class preJays:

    @staticmethod
    def parseConversation(line):
        items = line.split(";")
        d = dict()
        for attr in CONV_ATTRS:
            d[attr["attr_name"]] = preJays.getData(items[attr["index"]], attr["name"], attr["type"])
        return d

    @staticmethod
    def parseProfile(line):
        items = line.split(';')
        d = dict()
        for attr in PROF_ATTRS:
            d[attr["attr_name"]] = preJays.getData(items[attr["index"]], attr["name"], attr["type"])
        return d

    @staticmethod
    def getData(string, attr_name, type):
        if string in ["null", "0", "{}", "None"]:
            return None
        if attr_name:
            assert string.startswith(attr_name), \
                    "the string \"" + string + "\" doesn't start with the attribute name " + attr_name
            assert string[len(attr_name)] == ":"
            string = string[len(attr_name) + 1:]
        if type == "int":
            return int(string)
        elif type == "dict":
            return dict([(int(key[5:]), value) for key, value in json.loads(string).iteritems()])
        else:
            return string

    @staticmethod
    def readConversations():
        result = []
        with open(FOLDER + "/" + CONV_FILE, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if not line.startswith("#"):
                    result.append(preJays.parseConversation(line))
        return result

    @staticmethod
    def readProfiles():
        result = []
        with open(FOLDER + "/" + PROF_FILE, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if not line.startswith("#"):
                    result.append(preJays.parseProfile(line))
        return result

if __name__ == "__main__":
    out = preJays.readProfiles()
    print json.dumps(out, indent = 4)
