# all minds
import os

def load_mind(name):
    """
      use this to load `name` mind
    """
    mind=oa.mind.minds[name]
    mind.name=name
    mind.module=os.path.join(oa.cur_dir, 'mind', name+'.py')
    mind.cache_dir=os.path.join(oa.cur_dir, 'cache', name)
    # let's make dirs
    if not os.path.exists(mind.cache_dir):
        os.makedirs(mind.cache_dir)

    cf_data=fread(mind.module)
    d_exec=dict(oa.app.stub_funcs.items())
    exec(cf_data,d_exec)
    #let's add commands without spaces
#        _.kws=d_exec['kws']
    mind.kws={}#d_exec['kws']
    for key, value in d_exec['kws'].items():
        for synonym in key.strip().split(','):
            mind.kws[synonym]=value
        #_.kws[key.replace(' ','').replace('?','').replace("'",'')]=value

def set_mind(name, history=1):
    info('Switch mind: %s->%s'%(oa.mind.active.name,name))
    if history:
        info('switch_hist.append : '+name)
        switch_hist.append(name)
    oa.mind.active=oa.mind.minds[name]
    return oa.mind.active

def switch_back():
    """
      let's switch to previous `mind` (from switch_hist)
    """
    set_mind(switch_hist.pop(),0)

def load_minds():
    """
#      check dictionaries for all minds.
#      Handles updating the language using the online lmtool.
    """
    info('Load minds.\nPlease wait...')
    for mind in os.listdir(os.path.join(oa.cur_dir, 'mind')):
        if mind.lower().endswith('.py'):
            load_mind(mind[:-3])
    info('Done!')

def _in():
    global switch_hist
    # history for switch minds commands
    switch_hist=[]
#    hist_file=os.path.join(oa.cur_dir, 'history')
    load_minds()
    set_mind('boot')
    while oa.alive:
        text=get()
        info('text',text)
        mind=oa.mind.active
        info('%s.Command : %s'%(mind.name,text))
        if (text is None) or (text.strip()==''):
            #nothing to do
            continue
        t = text.lower()
        # Is There A Matching Command?
        fn=mind.kws.get(t,None)
#        info({'kws':mind.kws})
#        info({'fn':fn})
        if fn is not None:
            info('Perform : %s'%str(fn))
            oa.last_phrase=t
            #for now - 2 types of commands : Stub and Command line Text
            #for Stubs we will call perform
            if isCallable(fn):
                call_func(fn)
            #for string we will call sys_exec
            elif isinstance(fn,(str)):
                sys_exec(fn)
            else:
                #we have not idea what type of this command is, so we'll raise Exception
                info('Unkown command',str(fn))
                #raise Exception('Unkown command type : %s'%str(_.kws[t]))
#            fwrite(hist_file, 'mind %s:%s'%(t), append=True)
