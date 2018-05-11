# Open Assistant 0.03
# 2016 General Public License V3
# By Andrew Vavrek, Clayton G. Hobbs, Jezra, Jonathan Kulp

# core.py - Open Assistant System Core
import os, time
import threading
import oa_utils
from oa_utils import *

#subscribers- listeners will receive message from part
oa.ear.subs=[oa.stt]
oa.stt.subs=[oa.mind,oa.display]
oa.keyb.subs=[oa.mind,oa.display]

def _in(part):
    """
      processing messages using q_in
    """
    #subscribers
    if not isinstance(part.subs,list):
        raise Exception('Wrong Subs: '+part.name)

    fn=part._in
    info('started')
    for x in fn():#locals={'q_in':q_in}
#        info('Send to !sub:',sc.name)
        for sc in part.subs:
#            info('Send to !sub:',sc.name)
            info('Send to sub:',sc.name)
            sc.q_in.put(x)
#        continue
#        info(part.name,'_in data. len(data)=',len(x))
    info('closed')

class Assistant:
    def __init__(_):
        info("Initializing Assistant")
        # let's add link to OA itself
        oa.cur_dir=os.path.dirname(__file__)
        oa.app=_
#        oa.__dict__.update(oa_utils.__dict__)
        # stubs for functions of oa_utils
        _.stub_funcs=Stub.prepare_stubs(oa_utils)
        _.active = threading.Event()
        _.active.set()
        oa.alive=lambda : _.active.is_set()
        _.parts={}
        _.thread_pool=[]
        _.load_parts()

    def loop(_):#,condition=lambda : True):
        try:
            while oa.alive:# and condition():
                time.sleep(.1)
        except KeyboardInterrupt:
            info('attempting to close threads.')
            _.active.clear()
            [thr.join() for thr in _.thread_pool]
            info('threads successfully closed')

    def load_parts(_):
        #def full_path(name):
        #    return os.path.join(os.path.dirname(__file__),name)

        #get all In/Out operations from parts
        #load parts
        for pname in os.listdir('part'):
            info('Load part : '+pname)
            name=pname[:-3]
#            if name<>'ear':
#                continue
        #    cf_data=fread(full_path('parts/%s.py'%part))
            fdata=fread('part/'+pname)

            dinf=dict(list(oa_utils.__dict__.items())[:])
            #dinf={'oa':oa,'q_in':queue.Queue()}
            #add queues
            dinf['q_in']=queue.Queue()
            exec(fdata,dinf)
            part=AnyProp(**dinf)
            oa[name].__dict__.update(part.__dict__)
            part=oa[name]
            setattr(part,'name',name)
#            if name=='mind':
#                pass
            part.__dict__.setdefault('subs',[])
#                setattr(part,'subs',[])
#            print(oa.ear)
#            print(part)
#            _in(oa.ear)
#            return
            if dinf.get('_in',None) is not None:
                #additional check for yield
                if 'yield' not in fdata.lower():
                    info('WARNING: Please check part %s for yield in _in()'%name)
                #start process in
                thr=threading.Thread(target=_in, name=name, args=(part,))
#                thr.daemon=True
                _.parts[name]=part
                _.thread_pool.append(thr)

        #    p=threading.Thread(target=_in, args=(fn_in,part[:-3]))
        #    p.start()
        #    p.join()
        #start all together
#        for x in parts:
#            print(x.name,x.subs)
        [thr.start() for thr in _.thread_pool]


if __name__ == '__main__':
    Assistant().loop()
