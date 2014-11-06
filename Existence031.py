#!/usr/bin/env python3

interaction_valence = {
    ('e1', 'r1'): -1,
    ('e1', 'r2'): +1,
    ('e2', 'r1'): -1,
    ('e2', 'r2'): +1,
    }
all_experiments = ['e1', 'e2']

knownInteractions = {}
def learnCompositeInteraction(contextInteraction, enactedInteraction):
    if contextInteraction is None:
        return
    ci = (contextInteraction, enactedInteraction)
    knownInteractions[ci] = knownInteractions.get(ci, 0) + 1

def anticipate(enactedInteraction):
    #print('knownInteractions:', knownInteractions)
    anticipations = {} # experiment --> proclivity
    for ci in knownInteractions:
        if ci[0] == enactedInteraction:
            postInteraction = ci[1]
            proposedExperiment = postInteraction[0]
            weight = knownInteractions[ci]
            proclivity = weight * interaction_valence[postInteraction]
            anticipations[proposedExperiment] = anticipations.get(proposedExperiment, 0) + proclivity
    return anticipations

def selectExperiment(anticipations):
    print('anticipations:', anticipations)
    if not anticipations:
        return all_experiments[0]
    l = []
    for experiment in anticipations:
        proclivity = anticipations[experiment]
        l.append((proclivity, experiment))
    l.sort()
    proclivity, experiment = l[-1] # pick last (highest proclivity)
    if proclivity >= 0:
        return experiment
    else:
        # return another experiment
        for e in all_experiments:
            if e != experiment:
                return e

def run():
    enactedInteraction = None

    for cycle in range(25):
        contextInteraction = enactedInteraction
        anticipations = anticipate(enactedInteraction)
        experiment = selectExperiment(anticipations)

        # this is Environment031
        T1 = 8
        T2 = 15
        if cycle <= T1 or cycle > T2:
            if experiment == 'e1':
                result = 'r1'
            else:
                result = 'r2'
        else:
            if experiment == 'e1':
                result = 'r2'
            else:
                result = 'r1'

        enactedInteraction = (experiment, result)
        if interaction_valence[enactedInteraction] >= 0:
            mood = 'pleased'
        else:
            mood = 'pained'
        learnCompositeInteraction(contextInteraction, enactedInteraction)

        print('===', cycle, experiment, result, mood)

run()
