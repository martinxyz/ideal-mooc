#!/usr/bin/env python3
from collections import OrderedDict

# primitive interaction --> valence
# note: during learning, new (abstract) primitive interactions are added
primitive_interactions = OrderedDict([
    (('e1', 'r1'), -1),
    (('e1', 'r2'), +1),
    (('e2', 'r1'), -1),
    (('e2', 'r2'), +1),
    ])

primitive_experiments = ['e1', 'e2']

def getValence(interaction):
    if interaction not in primitive_interactions:
        pre, post = interaction
        return getValence(pre) + getValence(post)
    return primitive_interactions[interaction]

learned = OrderedDict() # compositeInteraction --> weight
def learn(pre, post):
    ci = (pre, post)
    learned[ci] = learned.get(ci, 0) + 1
    print('learned', pretty(ci), 'valence', getValence(ci), 'weight', learned[ci])

def anticipate(context):
    anticipations = OrderedDict() # experiment --> proclivity
    for i in primitive_experiments:
        anticipations[i] = 0

    for (pre, post), weight in learned.items():
        if pre in context:
            proclivity = weight * getValence(post)
            if post in primitive_interactions:
                experiment = post[0]
            else:
                experiment = post
            anticipations[experiment] = anticipations.get(experiment, 0) + proclivity
    return anticipations

def selectExperiment(anticipations):
    l = []
    for experiment in anticipations:
        proclivity = anticipations[experiment]
        l.append((proclivity, experiment))
    l.sort(key=lambda x: -x[0]) # sort by decreasing proclivity
    for proclivity, experiment in l:
        print('propose', pretty(experiment), 'proclivity', proclivity)
    return l[0][1] # pick experiment with highest proclivity

def enact(interaction):
    if interaction[0] in primitive_experiments:
        experiment = interaction[0]
        result = environmentGetResult(experiment)
        return (experiment, result)
    else:
        pre, post = interaction
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
    for cycle in range(50):

        context = [] # interactions that are considered "previous"
        if hist[-1]:
            context.append(hist[-1])
            if hist[-1] not in primitive_interactions:
                pre, post = hist[-1]
                context.append(post)
        if hist[-1] and hist[-2]:
            context.append((hist[-2], hist[-1]))
        print('context', [pretty(i) for i in context])

        anticipations = anticipate(context)
        experiment = selectExperiment(anticipations)
        print('trying experiment', pretty(experiment))
        if experiment in primitive_experiments:
            intendedInteraction = (experiment, None)
        else:
            intendedInteraction = experiment
        enacted = enact(intendedInteraction)
        print('enacted', pretty(enacted))

        if enacted != intendedInteraction and experiment not in primitive_experiments:
            # execution failed
            enacted = (experiment, enacted)
            if enacted not in primitive_interactions:
                # add a new primitive interaction
                primitive_interactions[enacted] = getValence(enacted[1])
            print('enacted really', pretty(enacted))

        if hist[-1]:
            learn(hist[-1], enacted)
        if hist[-1] and hist[-2]:
            learn(hist[-2], (hist[-1], enacted))
            learn((hist[-2], hist[-1]), enacted)
        hist.append(enacted)

        if getValence(enacted) >= 0:
            mood = 'pleased'
        else:
            mood = 'pained'

        print('===', cycle, pretty(enacted), mood)

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
