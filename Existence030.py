#!/usr/bin/env python3

interaction_valence = {
    ('e1', 'r1'): -1,
    ('e1', 'r2'): +1,
    ('e2', 'r1'): -1,
    ('e2', 'r2'): +1,
    }
all_experiments = ['e1', 'e2']

knownInteractions = []
def learnCompositeInteraction(contextInteraction, enactedInteraction):
    if contextInteraction is None:
        return
    ci = (contextInteraction, enactedInteraction)
    if ci not in knownInteractions:
        knownInteractions.append(ci)

def anticipate(enactedInteraction):
    anticipations = []
    for ci in knownInteractions:
        if ci[0] == enactedInteraction:
            anticipations.append(ci[1])
    return anticipations

def selectExperiment(anticipations):
    if not anticipations:
        return all_experiments[0]
    anticipations.sort(key=lambda a: interaction_valence[a])
    experiment, result = anticipations[-1] # pick last (highest valence)
    if interaction_valence[(experiment, result)] >= 0:
        return experiment
    else:
        for e in all_experiments:
            if e != experiment:
                return e

def run():
    enactedInteraction = None
    previousExperiment = None

    for cycle in range(13):
        contextInteraction = enactedInteraction
        anticipations = anticipate(enactedInteraction)
        experiment = selectExperiment(anticipations)

        # this is Environment030
        if experiment == previousExperiment:
            result = 'r1'
        else:
            result = 'r2'
        previousExperiment = experiment

        enactedInteraction = (experiment, result)
        if interaction_valence[enactedInteraction] >= 0:
            mood = 'pleased'
        else:
            mood = 'pained'
        learnCompositeInteraction(contextInteraction, enactedInteraction)

        print(cycle, experiment, result, mood)

run()
