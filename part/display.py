from cefpython3 import cefpython as cef
import base64
import platform
import sys, time
import threading

def set_javascript_bindings(browser):
    external = External(browser)
    bindings = cef.JavascriptBindings(bindToFrames=False, bindToPopups=False)
    bindings.SetObject("external", external)
    browser.SetJavascriptBindings(bindings)

#def browser_msg(browser, lang, event, msg):
#    # Execute Javascript function "js_print"
#    browser.ExecuteFunction("js_print", lang, event, msg)

import pyttsx3

class External(object):
    def __init__(_, browser):
        _.browser = browser

    def put(_, *args):
        print(args)

    def getVoices(_):#*args
        return oa.voice.voices

    def setVoice(_,VoiceId):#*args
        put('voice',('set_voice',VoiceId))

    def test_multiple_callbacks(_, js_callback):
        """Test both javascript and python callbacks."""
        js_print(_.browser, "Python", "test_multiple_callbacks",
                 "Called from Javascript. Will call Javascript callback now.")
#        def py_callback(msg_from_js):
#            js_print(self.browser, "Python", "py_callback", msg_from_js)
#        js_callback.Call("String sent from Python", py_callback)

def _in():
    cef.g_commandLineSwitches = {'enable-media-stream': '','allow-universal-access-from-files':''}
    cef.Initialize(settings={})
    browser = cef.CreateBrowserSync(url='file:///'+os.path.join(oa.cur_dir,'part/display/index.html'),
                                    window_title="Tutorial")
    set_javascript_bindings(browser)
    while oa.alive:
        pars=get(timeout=.01)
        cef.SingleMessageLoop()
        yield ''
        if pars is None:
            continue
#        browser.ExecuteFunction('oa_msg',str(pars))
        if isinstance(pars,(tuple,list)):
            browser.ExecuteFunction(*pars)
    cef.Shutdown()

def main():
    pass

if __name__ == '__main__':
    main()
