#!/usr/bin/env python3

def pickExperiment(painful=None):
    experiments = ['e1', 'e2']
    for e in experiments:
        if e != painful:
            return e

interaction_valence = {
    ('e1', 'r1'): -1,
    ('e1', 'r2'): +1,
    ('e2', 'r1'): -1,
    ('e2', 'r2'): +1,
    }

mood = 'pleased'
experiment = pickExperiment()

for cycle in range(11):
    if mood == 'pained':
        selfSatisfiedDuration = 0
        experiment = pickExperiment(painful=experiment)

    # this is Environment010
    if experiment == 'e1':
        result = 'r1'
    else:
        result = 'r2'

    interaction = (experiment, result)
    valence = interaction_valence[interaction]

    if valence >= 0:
        mood = 'pleased'
    else:
        mood = 'pained'

    print(cycle, experiment, result, mood)
