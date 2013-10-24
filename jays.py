#!/usr/bin/env python

import csv
import json
from random import random

FOLDER = "test-data"
CONV_FILE = "conversations_dataset"
PROF_FILE = "profiles_dataset.csv"

CONV_ATTRS = ("chat", "first_user_id", "second_user_id", \
        "first_user_profile_id", "second_user_profile_id")

def read_conversations():
    with open(FOLDER + "/" + CONV_FILE, "r") as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        reader = csv.DictReader(f, dialect = dialect)
        out = []
        for row in reader:
            out.append(row)
    return out

if __name__ == "__main__":
    out = read_conversations()
    print out[1]

