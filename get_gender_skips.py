from itertools import combinations_with_replacement

"""
Looks at each pair of M-F, F-F, etc., and gives percentage who skip.
Hack that takes advantage of ./train.py to run
"""

GENDER_DICT = {"M": 1, "F": 2, "None": 4}
def getGender(profiles, profile_id):
    if not profile_id in profiles:
        return "None"
    return str(profiles[profile_id]["gender"])

def dictify(profiles):
    return dict([(item["id"], item) for item in profiles])

"""
@param list of profiles
@param list of edges
@return list of thetas
"""
def train(profiles, convos):
    profiles = dictify(profiles)

    lists = dict()
    for g1, g2 in combinations_with_replacement(GENDER_DICT.values(), 2):
        lists[g1 + g2] = [0, 0]

    for convo in convos:
        profile1, profile2 = convo["profile1"], convo["profile2"]
        g1, g2 = GENDER_DICT[getGender(profiles, profile1)], GENDER_DICT[getGender(profiles, profile2)]
        length = convo["lines1"] if convo["lines1"] else 0 + convo["lines2"] if convo["lines2"] else 0
        lists[g1 + g2][int(length > 0)] += 1
    
    for g1, g2 in combinations_with_replacement(GENDER_DICT.values(), 2):
        print "%s: %s" % (g1 + g2, lists[g1 + g2][0] / float(lists[g1 + g2][0] + lists[g1 + g2][1]))

    return None

