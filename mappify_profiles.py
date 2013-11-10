#!/usr/bin/env python

from import_tool import importProfile

FOLDER = "small-data"
PROF_FILE = "json_profile_data"

def get_all():
    all_profiles = {}
    print "Loading profiles..."
    profiles = importProfile()
    print "Read in", len(profiles), "profiles"
    for prof in profiles:
        all_profiles[prof["id"]] = prof
    return all_profiles

def test():
    get_all()

if __name__ == "__main__":
    test()
