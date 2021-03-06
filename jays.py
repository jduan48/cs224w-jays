#!/usr/bin/env python

import csv
import json
import re
import time
from random import random

FOLDER = "data"
CONV_FILE = "conversations_dataset"
PROF_FILE = "profiles_dataset.csv"
OUTPUT_FOLDER = "small-data"
CONV_RESULT_FILE = "json_convo_data"
PROF_RESULT_FILE = "json_profile_data"
START_TIME = time.strptime("9/12/13 12:00", "%m/%d/%y %H:%M")
END_TIME = time.strptime("9/12/13 12:30", "%m/%d/%y %H:%M")

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
    used_profiles = set()

    @staticmethod
    def parseConversation(line, d):
        items = line.split(";")
        if not preJays.isValidTime(items):
            return False
        for attr in CONV_ATTRS:
            d[attr["attr_name"]] = preJays.getData(items[attr["index"]], attr["name"], attr["type"])
        preJays.used_profiles.add(d["profile1"])
        preJays.used_profiles.add(d["profile2"])
        return True

    @staticmethod
    def parseProfile(line, d):
        items = re.sub(r'&.*?;', '', line).split(';')
        if not preJays.isValidProfileId(items):
            return False
        for attr in PROF_ATTRS:
            d[attr["attr_name"]] = preJays.getData(items[attr["index"]], attr["name"], attr["type"])
        return True

    #check if this profile has been involved in a conversation in our subset
    @staticmethod
    def isValidProfileId(items):
        if preJays.getData(items[0], PROF_ATTRS[0]["name"], PROF_ATTRS[0]["type"]) not in preJays.used_profiles:
            return False
        return True

    @staticmethod
    def isValidTime(items):
        string = items[5]
        convo_time = time.strptime(string, "%a %b %d %Y %H:%M:%S GMT+0000 (UTC)")
        return convo_time > START_TIME and convo_time < END_TIME

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
    def readData(input_file, output_file, parser):
        open(OUTPUT_FOLDER + "/" + output_file, 'w').close()
        with open(OUTPUT_FOLDER + "/" + output_file, 'a') as outfile:
            with open(FOLDER + "/" + input_file, "r") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if not line.startswith("#"):
                        d = {}
                        if parser(line, d):
                            json.dump(d, outfile)
                            outfile.write('\n')

if __name__ == "__main__":
    convos = preJays.readData(CONV_FILE, CONV_RESULT_FILE, preJays.parseConversation)
    profiles = preJays.readData(PROF_FILE, PROF_RESULT_FILE, preJays.parseProfile)
