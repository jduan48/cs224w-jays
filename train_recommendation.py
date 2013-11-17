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

"""
given two profiles, predict the similarity between two profiles
"""
def getSimilarity(profile1, profile2, profiles):
    return 1

"""
Given the user profiles, predict how much the number of lines from profile1
to profile2 deviates from the average
"""

PRINT = 10
def getUserDelta(profile1, profile2, user_delta, profiles):
    if not str(profile1) in user_delta:
        return 0
    print "DOING", profiles[str(profile1)]
    if PRINT:
        for profile, line in user_delta[str(profile)]:
            print line, profiles[profile]
        PRINT -= 1

    weights = dict([(profile, getSimilarity(profile2, profile, profiles)) for (profile, line) in user_delta[str(profile1)]])
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
    print global_avg
    for id1, id2, profile1, profile2 in convos:
        user1_prediction = getUserDelta(profile1, profile2, user_delta, profiles) + global_avg +\
                user_avg[str(profile1)] if str(profile1) in user_avg else 0
        user2_prediction = getUserDelta(profile2, profile1, user_delta, profiles) + global_avg +\
                user_avg[str(profile2)] if str(profile2) in user_avg else 0
        result.append(user1_prediction + user2_prediction)
    return result





