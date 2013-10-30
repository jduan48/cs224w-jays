"""
@param list of profiles
@param list of edges
@return list of thetas
"""
def train(profiles, convos):
    result = {}
    global_convos = []
    for convo in convos:
        user1, user2 = str(convo["user1"]), str(convo["user2"])
        length = convo["lines1"] if convo["lines1"] else 0 + convo["lines2"] if convo["lines2"] else 0
        for user in [user1, user2]:
            if not user in result:
                result[user] = []
            result[user].append(length)
        global_convos.append(length)
    return dict(\
        users = dict((user, float(sum(convos)) / len(convos)) for (user, convos) in result.iteritems())
        global_average = float(sum(global_convos)) / len(global_average))

"""
Supports different feature-vector lengths for men and women.
@param list of profiles
@param list of conversations
@param list of thetas
@return predicted length of conversation
"""
def predict(profiles, convos, thetas):
    result = []
    users, global_average = thetas["users"], thetas["global_average"]
    for user1, user2 in convos:
        total = 0
        for user in user1, user2:
            if user in users:

        user1, user2 = str(male), str(female)
        if user1 in thetas and user2 in thetas:
            prediction = (thetas[user1] + thetas[user2]) / 2.0
        else:
            prediction = 20
        result.append(prediction)
    return result
