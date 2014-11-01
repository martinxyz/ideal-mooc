#!/usr/bin/env python3

def pickExperiment(dislike=None):
    experiments = ['e1', 'e2']
    for e in experiments:
        if e != dislike:
            return e

interaction_valence = {
    ('e1', 'r1'): -1,
    ('e1', 'r2'): +1,
    ('e2', 'r1'): -1,
    ('e2', 'r2'): +1,
    }

stored_interactions = {} # experiment --> result
selfSatisfiedDuration = 0
mood = 'self-satisfied'
experiment = pickExperiment()

for cycle in range(13):
    if mood == 'pained':
        experiment = pickExperiment(dislike=experiment)
    elif mood == 'bored':
        selfSatisfiedDuration = 0
        experiment = pickExperiment(dislike=experiment)

    # anticipate the stored result (possibly None)
    anticipatedResult = stored_interactions.get(experiment)

    # this is Environment010
    if experiment == 'e1':
        result = 'r1'
    else:
        result = 'r2'

    interaction = (experiment, result)
    valence = interaction_valence[interaction]

    if result == anticipatedResult and valence >= 0: 
        mood = 'self-satisfied'
        selfSatisfiedDuration += 1
        if selfSatisfiedDuration > 3:
            mood = 'bored'
    else:
        if valence >= 0:
            mood = 'pleased'
        else:
            mood = 'pained'

    stored_interactions[experiment] = result

    print(cycle, experiment, result, mood)
