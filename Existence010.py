#!/usr/bin/env python3

stored_interactions = {} # experiment --> result
selfSatisfactionCounter = 0
selfSatisfiedDuration = 0
experiment = 'e1'
mood = 'self-satisfied'

def pickExperiment(boring=None):
    experiments = ['e1', 'e2']
    for e in experiments:
        if e != boring:
            return e

experiment = pickExperiment()

for cycle in range(11):
    if mood == 'bored':
        selfSatisfiedDuration = 0
        experiment = pickExperiment(boring=experiment)

    # anticipate the stored result (possibly None)
    anticipatedResult = stored_interactions.get(experiment)

	# this is Environment010
    if experiment == 'e1':
        result = 'r1'
    else:
        result = 'r2'

    if experiment not in stored_interactions:
        stored_interactions[experiment] = result
     
    if result == anticipatedResult: 
        mood = 'self-satisfied'
        selfSatisfiedDuration += 1
    else:
        mood = 'frustrated'
        selfSatisfiedDuration = 0

    if selfSatisfiedDuration > 3:
        mood = 'bored'

    print(cycle, experiment, result, mood)
