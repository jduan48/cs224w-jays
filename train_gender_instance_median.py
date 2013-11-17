###
# For each user, finds average length of their conversations with males, females, and unreported.
# If user wasn't trained upon, returns global average.
# Potential bug - if user didn't have a conversation with males/females/unreported, they're assigned 0
###

from itertools import combinations_with_replacement
from numpy import median
from collections import defaultdict

GENDER_DICT = {"M": 1, "F": 2, "None": 4}
def getGender(profiles, profile_id):
    if not profile_id in profiles:
        return "None"
    return str(profiles[profile_id]["gender"])

"""
@param list of profiles
@param list of edges
@return list of thetas
thetas[user][gender] = [count, total]
"""
def train(profiles, convos):
    result = {}
    global_avgs = defaultdict(list)
    
    for convo in convos:
        user1, user2 = convo["profile1"], convo["profile2"]
        length = convo["lines1"] if convo["lines1"] else 0 + convo["lines2"] if convo["lines2"] else 0
        
        for user in [user1, user2]:
            if not user in result:
                result[user] = defaultdict(list)
                
        user1_gender = GENDER_DICT[getGender(profiles, user1)]
        user2_gender = GENDER_DICT[getGender(profiles, user2)]
        result[user1][user2_gender].append(length)
        result[user2][user1_gender].append(length)
        
        global_avgs[user1_gender].append(length)
        global_avgs[user2_gender].append(length)
    
    for user, genders in result.iteritems():
        for gender in genders.keys():
            result[user][gender] = median(result[user][gender]) if result[user][gender] else 0
    for key, val in global_avgs.iteritems():
        global_avgs[key] = median(val)
        
    return (result, global_avgs)

"""
Supports different feature-vector lengths for men and women.
@param list of profiles
@param list of conversations
@param list of thetas
@return predicted length of conversation
"""
def predict(profiles, convos, thetas):
    global_avgs = thetas[1]
    thetas = thetas[0]
    result = []
    for id1, id2, profile1, profile2 in convos:
        g1, g2 = GENDER_DICT[getGender(profiles, profile1)], GENDER_DICT[getGender(profiles, profile2)]
        user1_prediction = thetas[str(profile1)][str(g2)] if profile1 in thetas else global_avgs[str(g1)]
        user2_prediction = thetas[str(profile2)][str(g1)] if profile2 in thetas else global_avgs[str(g2)]
        result.append((user1_prediction + user2_prediction) / 2.0)
    return result
