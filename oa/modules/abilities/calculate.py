from itertools import groupby

import oa.legacy

from oa.modules.abilities.core import info
from oa.modules.abilities.interact import say

def isNum(s):
    return s.replace('.', '').isdigit()

def expr2str():
    """ Convert a numerical expression into a string. """
    ret = ''
    info(oa.legacy.sys.calc_opers.values())
    for k, g in groupby(oa.legacy.sys.expr, lambda x: ((x in oa.legacy.sys.calc_opers.values()) and 1) or 2):
        l=list(g)
        if len(l) > 1:
            if k == 1:
                raise Exception('two opers')
            else:
                sr='(' + l[0]
                for x in l[1:]:
                    if isNum(x):
                        sr += '+' + x
                    else:
                        # 'hundreds, thousands so on'
                        sr += x
                ret += sr + ')'
        else:
            ret += l[0]
    return ret

def add2expr(s):
    # Check for calculator. Move to a numbers definition file.
    # For numbers, add sum operator.
    oa.legacy.sys.expr.append(s)

def calculate():
    ret = expr2str()
    info(oa.legacy.op.sys.expr)
    info('expr=' + ret)
    try:
        say(eval(ret))
    except:
        say('Error. Wrong expression. ' + ret)
    # Clear the expression.
    oa.legacy.sys.expr = []