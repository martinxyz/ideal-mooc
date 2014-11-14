#!/usr/bin/env python3

# TODO: not yet working

interaction_valence = {
    ('e1', 'r1'): -1,
    ('e1', 'r2'): +1,
    ('e2', 'r1'): -1,
    ('e2', 'r2'): +1,
    }
primitive_experiments = ['e1', 'e2']
primitive_interactions = sorted(interaction_valence.keys())

learned = {} # compositeInteraction --> weight
def learnCompositeInteraction(pre, post):
    ci = (pre, post)
    learned[ci] = learned.get(ci, 0) + 1
    if ci not in interaction_valence:
        interaction_valence[ci] = interaction_valence[pre] + interaction_valence[post]
    print('learned', pretty(ci), 'weight', learned[ci])

def anticipate(context):
    anticipations = {} # experiment --> proclivity
    for i in primitive_experiments:
        anticipations[i] = 0

    for pre, post in learned:
        if pre in context:
            proposedExperiment = post[0]
            weight = learned[(pre, post)]
            proclivity = weight * interaction_valence[post]
            anticipations[proposedExperiment] = anticipations.get(proposedExperiment, 0) + proclivity
    return anticipations

def selectExperiment(anticipations):
    l = []
    for experiment in anticipations:
        print('  anticipation', pretty(experiment))
        proclivity = anticipations[experiment]
        l.append((proclivity, experiment))
    l.sort(key=lambda x: x[0]) # sort by proclivity
    l.reverse()
    for proclivity, experiment in l:
        print('propose', pretty(experiment), 'proclivity', proclivity)
    return l[0][1] # pick experiment with highest proclivity

def enact(experiment):
    #print('enacting', pretty(experiment))
    if experiment in primitive_experiments:
        result = environmentGetResult(experiment)
        return (experiment, result)
    else:
        pre, post = experiment
        enacted = enact(pre)
        if enacted != pre:
            return enacted
        else:
            return (pre, enact(post))

# this is Environment040
envHist = [None, None]
def environmentGetResult(experiment):
    result = 'r1'
    if envHist[-2] != experiment and envHist[-1] == experiment:
        result = 'r2'
    envHist.append(experiment)
    return result

def run():
    hist = [None, None] # history of enacted interactions
    for cycle in range(25):

        context = [] # interactions that are considered "previous"
        if hist[-1]:
            context.append(hist[-1])
            if hist[-1] not in primitive_interactions:
                pre, post = hist[-1]
                context.append(post)
        if hist[-1] and hist[-2]:
            context.append((hist[-2], hist[-1]))

        anticipations = anticipate(context)
        experiment = selectExperiment(anticipations)
        enactedInteraction = enact(experiment)
        print('enacted', pretty(enactedInteraction))

        if hist[-1]:
            learnCompositeInteraction(hist[-1], enactedInteraction)
        if hist[-1] and hist[-2]:
            learnCompositeInteraction((hist[-2], hist[-1]), enactedInteraction )
            learnCompositeInteraction(hist[-2], (hist[-1], enactedInteraction))
        hist.append(enactedInteraction)

        if interaction_valence[enactedInteraction] >= 0:
            mood = 'pleased'
        else:
            mood = 'pained'

        print('===', cycle, pretty(enactedInteraction), mood)

def pretty(thing):
    if isinstance(thing, str):
        return thing
    else:
        a, b = thing
        if not isinstance(a, str):
            a = '<' + pretty(a) + '>'
        if not isinstance(b, str):
            b = '<' + pretty(b) + '>'
        return a + b

run()
