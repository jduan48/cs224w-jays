import math, random
from import_tool import *

def train(profiles, convos):
    global_vector, user_vector = [], dict()
    for convo in convos:
        for user, line in [(convo["profile1"], convo["lines1"]), (convo["profile2"], convo["lines2"])]:
            if not line:
                line = 0
            if not user in user_vector:
                user_vector[user] = []
            user_vector[user].append(line)
            global_vector.append(line)
    global_avg = float(sum(global_vector)) / len(global_vector)
    user_avg = dict([(key, float(sum(value)) / len(value) - global_avg) for (key, value) in user_vector.iteritems()])

    user_delta = dict()
    for convo in convos:
        for user1, user2, line in [(convo["profile1"], convo["profile2"], convo["lines1"]),
                (convo["profile2"], convo["profile1"], convo["lines2"])]:
            if not user1 in user_delta:
                user_delta[user1] = []
            if not line:
                line = 0
            user_delta[user1].append((user2, line - global_avg - user_avg[user1]))
    return dict(global_avg = global_avg,
                user_avg = user_avg,
                user_delta = user_delta)

COUNTRIES = importCountries()

def getLocationSimilarity(profile1, profile2):
    # if the users from the same country
    loc1 = profile1["location"].split(" ")[-1] if profile1.get("location") else ""
    loc2 = profile2["location"].split(" ")[-1] if profile2.get("location") else ""
    if not (loc1 and loc2 and loc1 in COUNTRIES and loc2 in COUNTRIES):
        return 0.1

    c1, c2 = COUNTRIES[loc1], COUNTRIES[loc2]
    if c1 == c2:
        return 1
    if c1["subregion"] == c2["subregion"]:
        return .9
    if c1["region"] == c2["region"]:
        return .8
    if c1["language"] == c2["language"]:
        return .3
    return 0.1

def getAgeSimilarity(profile1, profile2):
    # if the users are similar in age
    age1, age2 = profile1.get("age"), profile2.get("age")
    if not (age1 and age2):
        return .5
    return max(1 - abs(math.log(profile1["age"], 2) - math.log(profile2["age"], 2)), 0.1)

def getAboutSimilarity(profile1, profile2):
    # if the users have similar descriptions
    about1, about2 = profile1.get("about"), profile2.get("about")
    if not (about1 and about2):
        return 0
    set1, set2 = set(about1.keys()), set(about2.keys())
    return float(len(set1 & set2)) / len(set1 | set2) if set1 or set2 else 0

"""
given two profiles, predict the similarity between two profiles
"""
def getSimilarity(profile1, profile2, profiles):
    profile1, profile2 = profiles[profile1], profiles[profile2]

    location_sim = getLocationSimilarity(profile1, profile2)
    about_sim = getAboutSimilarity(profile1, profile2)
    age_sim = getAgeSimilarity(profile1, profile2)

    sim = .9 * about_sim + .05 * age_sim + .05 * location_sim

    return sim

"""
Given the user profiles, predict how much the number of lines from profile1
to profile2 deviates from the average
"""
def getUserDelta(profile1, profile2, user_delta, profiles):
    if not str(profile1) in user_delta or not profile1 in profiles:
        return 0
    weights = dict([(profile, getSimilarity(profile2, profile, profiles)) for (profile, line) in user_delta[str(profile1)]])
    if random.randint(1, 100) == 3:
        print len(weights.keys())
    return float(sum([line * weights[profile] for (profile, line) in user_delta[str(profile1)]])) / sum(weights.values())

"""
Supports different feature-vector lengths for men and women.
@param list of profiles
@param list of conversations
@param list of thetas
@return predicted length of conversation
"""
def predict(profiles, convos, thetas):
    result = []
    global_avg, user_avg, user_delta = thetas["global_avg"], thetas["user_avg"], thetas["user_delta"]
    for id1, id2, profile1, profile2 in convos:
        if random.randint(1, 100) == 4:
            if str(profile1) in user_avg and str(profile2) in user_avg:
                print "in"
            else:
                print "out"
        user1_prediction = getUserDelta(profile1, profile2, user_delta, profiles) + global_avg +\
                user_avg[str(profile1)] if str(profile1) in user_avg else 0
        user2_prediction = getUserDelta(profile2, profile1, user_delta, profiles) + global_avg +\
                user_avg[str(profile2)] if str(profile2) in user_avg else 0
        result.append(user1_prediction + user2_prediction)
    return result
