opers="""
plus:+
minus:-
multiply:*
divide://
logarithm:math.log
pi:math.pi
power:**
point:.
square:**0.5
"""
sys_info.expr=''

kws={
  'equal':calculate(),
  'quit':quit_app()
}

kws.update(_lines_to_dict(_fread('nums'), add2expr))
kws.update(_lines_to_dict(opers,add2expr))
