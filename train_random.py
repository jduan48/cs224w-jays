import random 

"""
@param list of profiles
@param list of edges
@return list of thetas
"""
def train(profiles, convos):
    return [convo["lines1"] if convo["lines1"] else 0 + \
            convo["lines2"] if convo["lines2"] else 0 for convo in convos]

"""
Supports different feature-vector lengths for men and women.
@param list of profiles
@param list of conversations
@param list of thetas
@return predicted length of conversation
"""
def predict(profiles, convos, thetas):
    return [random.choice(thetas) for convo in convos]