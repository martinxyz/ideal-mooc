#!/usr/bin/env python3
from collections import OrderedDict

# primitive interaction --> valence
primitive_interactions = OrderedDict([
    (('e1', 'r1'), -1),
    (('e1', 'r2'), +1),
    (('e2', 'r1'), -1),
    (('e2', 'r2'), +1),
    ])
primitive_experiments = ['e1', 'e2']

class CompositeInteraction(tuple):
    "an interaction of the form (preInteraction, postInteraction)"
    pass # it's just a tuple

def getValence(interaction):
    if isinstance(interaction, CompositeInteraction):
        pre, post = interaction
        return getValence(pre) + getValence(post)
    else:
        experiment, result = interaction
        if interaction not in primitive_interactions:
            return getValence(result)
        else:
            return primitive_interactions[interaction]

learned = OrderedDict() # compositeInteraction --> weight
def learn(pre, post):
    ci = CompositeInteraction((pre, post))
    learned[ci] = learned.get(ci, 0) + 1
    print('learned', pretty(ci), 'valence', getValence(ci), 'weight', learned[ci])

def anticipate(context):
    anticipations = OrderedDict() # experiment --> proclivity
    for e in primitive_experiments:
        anticipations[e] = 0

    for (pre, post), weight in learned.items():
        if pre in context:
            proclivity = weight * getValence(post)
            if isinstance(post, CompositeInteraction):
                experiment = post # propose to re-enact the whole thing
            else:
                experiment = post[0] # it's an (experiment, result) interaction
            anticipations[experiment] = anticipations.get(experiment, 0) + proclivity
    return anticipations

def selectExperiment(anticipations):
    l = list(anticipations.items())
    l.sort(key=lambda x: -x[1]) # sort by decreasing proclivity
    for experiment, proclivity in l:
        print('propose', pretty(experiment), 'proclivity', proclivity)
    return l[0][0] # pick experiment with highest proclivity

def enact(interaction):
    if isinstance(interaction, CompositeInteraction):
        pre, post = interaction
        enacted = enact(pre)
        if enacted != pre:
            return enacted
        else:
            return CompositeInteraction((pre, enact(post)))
    else:
        experiment, result = interaction
        if experiment in primitive_experiments:
            result = environmentGetResult(experiment)
        else:
            result = enact(experiment)
        return (experiment, result)

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
    for cycle in range(30):
        context = [] # interactions that are considered "previous"
        if hist[-1]:
            context.append(hist[-1])
            if isinstance(hist[-1], CompositeInteraction):
                pre, post = hist[-1]
                context.append(post)
        if hist[-1] and hist[-2]:
            context.append(CompositeInteraction((hist[-2], hist[-1])))
        print('context', [pretty(i) for i in context])

        anticipations = anticipate(context)
        experiment = selectExperiment(anticipations)
        print('attempt', pretty(experiment))
        if experiment in primitive_experiments:
            intendedInteraction = (experiment, None)
        else:
            intendedInteraction = experiment
        enacted = enact(intendedInteraction)
        print('enacted', pretty(enacted), 'valence', getValence(enacted))

        if enacted != intendedInteraction and experiment not in primitive_experiments:
            # execution of composite interaction failed
            enacted = (experiment, enacted) # 'enacted' is the result
            print('enacted really', pretty(enacted))

        if hist[-1]:
            learn(hist[-1], enacted)
        if hist[-1] and hist[-2]:
            learn(hist[-2], CompositeInteraction((hist[-1], enacted)))
            learn(CompositeInteraction((hist[-2], hist[-1])), enacted)
        hist.append(enacted)

        if getValence(enacted) >= 0:
            mood = 'pleased'
        else:
            mood = 'pained'

        print('===', cycle, pretty(enacted), mood)

def pretty(thing):
    if isinstance(thing, str):
        return thing
    a, b = thing
    if isinstance(thing, CompositeInteraction):
        return '<' + pretty(a) + pretty(b) + '>'
    if thing in primitive_interactions:
        return pretty(a) + pretty(b)
    return ('(' + pretty(a) + '|' + pretty(b) + ')').upper()

run()
