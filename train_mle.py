"""
@param list of profiles
@param list of edges
@return list of thetas
"""
def train(profiles, convos):
    result = {}
    for profile in profiles:
        result[str(profile[0])] = {
                'num_convos': 0,
                'total_convo_length': 0,
            }
    for convo in convos:
        result[str(convo[1])]['num_convos'] += 1
        result[str(convo[1])]['total_convo_length'] += convo[11]
        result[str(convo[2])]['num_convos'] += 1
        result[str(convo[2])]['total_convo_length'] += convo[10]
    return result

"""
Supports different feature-vector lengths for men and women.
@param list of profiles
@param list of conversations
@param list of thetas
@return predicted length of conversation
"""
def predict(profiles, convos, thetas):
    result = [None] * len(convos)
    for i, (m, f) in enumerate(convos):
        m_score = (thetas[str(m)]['total_convo_length'] /
                float(thetas[str(m)]['num_convos']))
        f_score = (thetas[str(f)]['total_convo_length'] /
                float(thetas[str(f)]['num_convos']))
        result[i] = min(m_score, f_score)
    return result
