opers="""
plus:+
minus:-
multiply:*
divide://
logarithm:math.log
pi:math.pi
power:**
point,dot:.
square:**0.5
open:(
close:)
"""
oa.sys.expr=[]

kws={
  'equal, result':calculate(),
  'home':say('back to boot') & mind('boot'),
  'quit':quit_app()
}

oa.sys.calc_opers=_lines_to_dict(opers)
kws.update(_lines_to_dict(_fread('nums'), add2expr))
kws.update(_lines_to_dict(opers,add2expr))
