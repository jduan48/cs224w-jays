###
# For each user, finds average length of their conversations with males, females, and unreported.
# If user wasn't trained upon, returns global average.
# Potential bug - if user didn't have a conversation with males/females/unreported, they're assigned 0
###

from itertools import combinations_with_replacement

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
thetas[user][gender] = [count, total]
"""
def train(profiles, convos):
    profiles = dictify(profiles)
    
    result = {}
    all_convos = []
    
    for convo in convos:
        user1, user2 = str(convo["user1"]), str(convo["user2"])
        length = convo["lines1"] if convo["lines1"] else 0 + convo["lines2"] if convo["lines2"] else 0
        
        for user in [user1, user2]:
            if not user in result:
                result[user] = {}
                for g in GENDER_DICT.values():
                    result[user][g] = [0,0]  
        user1_gender = GENDER_DICT[getGender(profiles, user1)]
        user2_gender = GENDER_DICT[getGender(profiles, user2)]
        result[user1][user2_gender] = [result[user1][user2_gender][0] + 1, result[user1][user2_gender][1] + length]
        result[user2][user1_gender] = [result[user2][user1_gender][0] + 1, result[user2][user1_gender][1] + length]
        all_convos.append(length)
    return {"thetas":result, "global_average":(sum(all_convos) / float(len(all_convos)))}

def getUserPrediction(id1, id2, gender, thetas, global_avg):
    if id1 in thetas:
        if not thetas[id1][str(gender)][0]:
            return thetas[id1][str(gender)][1] / thetas[id1][str(gender)][0]
        #otherwise, get person's avg conversation length
        convo_lengths = [thetas[id1][str(g)][1] for g in GENDER_DICT.values() if thetas[id1][str(g)][0]]
        return (total / float(num_values)) if num_values else global_avg
    return global_avg

"""
Supports different feature-vector lengths for men and women.
@param list of profiles
@param list of conversations
@param list of thetas
@return predicted length of conversation
"""
def predict(profiles, convos, thetas):
    result = []
    global_avg = thetas["global_average"]
    thetas = thetas["thetas"]
    for id1, id2, profile1, profile2 in convos:
        g1, g2 = GENDER_DICT[getGender(profiles, profile1)], GENDER_DICT[getGender(profiles, profile2)]
        user1_prediction = getUserPrediction(id1, id2, g2, thetas, global_avg)
        user2_prediction = getUserPrediction(id2, id1, g1, thetas, global_avg)
        result.append((user1_prediction + user2_prediction) / 2.0)
    return result
