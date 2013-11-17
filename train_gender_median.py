from itertools import combinations_with_replacement
from numpy import median

GENDER_DICT = {"M": 1, "F": 2, "None": 4}
def getGender(profiles, profile_id):
    if not profile_id in profiles:
        return "None"
    return str(profiles[profile_id]["gender"])

"""
@param list of profiles
@param list of edges
@return list of thetas
"""
def train(profiles, convos):

    lists = dict()
    for g1, g2 in combinations_with_replacement(GENDER_DICT.values(), 2):
        lists[g1 + g2] = []

    for convo in convos:
        profile1, profile2 = convo["profile1"], convo["profile2"]
        g1, g2 = GENDER_DICT[getGender(profiles, profile1)], GENDER_DICT[getGender(profiles, profile2)]
        lists[g1 + g2].append(convo["lines1"] if convo["lines1"] else 0 + convo["lines2"] if convo["lines2"] else 0)
    thetas = {}
    for (key, lengths) in lists.iteritems():
        thetas[key] = median(lengths)
    return thetas

"""
Supports different feature-vector lengths for men and women.
@param list of profiles
@param list of conversations
@param list of thetas
@return predicted length of conversation
"""
def predict(profiles, convos, thetas):
    result = []

    for id1, id2, profile1, profile2 in convos:
        g1, g2 = GENDER_DICT[getGender(profiles, profile1)], GENDER_DICT[getGender(profiles, profile2)]
        result.append(thetas[str(g1 + g2)])
    return result
