"""
@param list of profiles
@param list of edges
@return list of thetas
"""
def train(profiles, convos):
    return sum([convo["lines1"] if convo["lines1"] else 0 + \
                convo["lines2"] if convo["lines2"] else 0 for convo in convos]) \
                / float(len(convos))
    

"""
Supports different feature-vector lengths for men and women.
@param list of profiles
@param list of conversations
@param list of thetas
@return predicted length of conversation
"""
def predict(profiles, convos, thetas):
    if not thetas:
        assert "No length for theta!"
    return [thetas,] * len(convos)
