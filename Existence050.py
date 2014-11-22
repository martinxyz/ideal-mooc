#!/usr/bin/env python3
from collections import OrderedDict

# primitive interaction --> valence
primitive_interactions = OrderedDict([
    ('e1r1', -1),
    ('e1r2', +1),
    ('e2r1', -1),
    ('e2r2', +1),
    ])
default_interactions = ['e1r2', 'e2r2']

failed_interactions = OrderedDict() # attempted interaction --> list of actual interactions

def getValence(interaction):
    if interaction in primitive_interactions:
        return primitive_interactions[interaction]
    pre, post = interaction
    return getValence(pre) + getValence(post)

learned = OrderedDict() # composite interaction --> weight
def learn(pre, post):
    ci = (pre, post)
    learned[ci] = learned.get(ci, 0) + 1
    print('learned', pretty(ci), 'valence', getValence(ci), 'weight', learned[ci])

def anticipate(context):
    anticipations = OrderedDict() # interaction --> proclivity
    for interaction in default_interactions:
        anticipations[interaction] = 0

    activated = []
    for (pre, post), weight in learned.items():
        if pre in context:
            activated.append((post, weight))

    for post, weight in activated:
        interaction = post # proposed interaction
        proclivity = weight * getValence(interaction)
        anticipations[interaction] = anticipations.get(interaction, 0) + proclivity

    for interaction in anticipations:
        for enacted in failed_interactions.get(interaction, []):
            for post, weight in activated:
                if enacted == post:
                    proclivity = weight * getValence(post)
                    anticipations[interaction] = anticipations.get(interaction, 0) + proclivity
    return anticipations

def selectInteraction(anticipations):
    l = list(anticipations.items())
    l.sort(key=lambda x: -x[1]) # sort by decreasing proclivity
    for interaction, proclivity in l:
        print('propose', pretty(interaction), 'proclivity', proclivity)
    return l[0][0] # pick interaction with highest proclivity

def enact(interaction):
    if interaction in primitive_interactions:
        return environmentEnact(interaction)
    pre, post = interaction
    enacted = enact(pre)
    if enacted != pre:
        return enacted
    else:
        return (pre, enact(post))

# this is Environment040
env_hist = [None, None]
def environmentEnact(interaction):
    assert interaction in primitive_interactions
    result = 'r1'
    experiment = interaction[:2]
    if env_hist[-2] != experiment and env_hist[-1] == experiment:
        result = 'r2'
    env_hist.append(experiment)
    return experiment + result

def run():
    hist = [None, None] # history of enacted interactions
    for cycle in range(60):
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
        intended = selectInteraction(anticipations)
        print('attempt', pretty(intended))
        enacted = enact(intended)
        print('enacted', pretty(enacted), 'valence', getValence(enacted))

        if enacted != intended:
            l = failed_interactions.get(intended, [])
            if enacted not in l:
                print('observed this unexpected outcome for the first time')
                l.append(enacted)
                failed_interactions[intended] = l

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
    if thing in primitive_interactions:
        return str(thing)
    a, b = thing
    return '<' + pretty(a) + ',' + pretty(b) + '>'

run()
