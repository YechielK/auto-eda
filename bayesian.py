import pandas as pd
import numpy as np
import scipy.stats as stats
from flask import g


def inverse(var, values):
    values['not_' + var] = 1 - values[var]

def calculate(a, bga, bgna):
    print(a, bga, bgna)
    values = {
        'a': float(a),
        'b_given_a': float(bga),
        'b_given_not_a': float(bgna)
    }

    # inverse
    inverse('a', values)
    inverse('b_given_a', values)
    inverse('b_given_not_a', values)

    values['b_and_a'] = values['b_given_a'] * values['a']
    values['not_b_and_a'] = values['not_b_given_a'] * values['a']
    values['b_and_not_a'] = values['b_given_not_a'] * values['not_a']
    values['not_b_and_not_a'] = values['not_b_given_not_a'] * values['not_a']

    values['b'] = values['b_given_a'] * values['a'] + values['b_given_not_a'] * values['not_a']
    inverse('b', values)

    values['a_given_b'] = values['b_and_a'] / values['b']
    values['not_a_given_b'] = values['b_and_not_a'] / values['b']
    values['a_given_not_b'] = values['not_b_and_a'] / values['not_b']
    values['not_a_given_not_b'] = values['not_b_and_not_a'] / values['not_b']



    # print(values)
    values = {k: round(v, 3) for k,v in values.items()}
    # print(fixed)

    return values



