# Tutorial example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+

from cefpython3 import cefpython as cef
import base64
import platform
import sys
import threading

# HTML code. Browser will navigate to a Data uri created
# from this html code.
HTML_code = """
<!DOCTYPE html>
<html>
<head>
    <style type="text/css">
    body,html { font-family: Arial; font-size: 11pt; }
    div.msg { margin: 0.2em; line-height: 1.4em; }
    b { background: #ccc; font-weight: bold; font-size: 10pt;
        padding: 0.1em 0.2em; }
    b.Python { background: #eee; }
    i { font-family: Courier new; font-size: 10pt; border: #eee 1px solid;
        padding: 0.1em 0.2em; }
    </style>
    <script>

    function js_print(lang, event, msg) {
        msg = "<b class="+lang+">"+lang+": "+event+":</b> " + msg;
        console = document.getElementById("console")
        console.innerHTML += "<div class=msg>"+msg+"</div>";
    }

    function put(data) {
        msg = "<b class="+lang+">"+data+"</b>";
        console = document.getElementById("console")
        console.innerHTML += "<div class=msg>"+msg+"</div>";
    }

    window.onload = function(){
//        js_print("Javascript", "window.onload", "Called");
//        js_print("Javascript", "python_property", python_property);
//        js_print("Javascript", "navigator.userAgent", navigator.userAgent);
//        js_print("Javascript", "cefpython_version", cefpython_version.version);
//        html_to_data_uri("test", js_callback_1);
        external.put(1,2,3,4,5);
    };
    </script>
</head>
<body>
    <h1>Tutorial example</h1>
    <div id="console"></div>
</body>
</html>
"""

def html_to_data_uri(html, js_callback=None):
    # This function is called in two ways:
    # 1. From Python: in this case value is returned
    # 2. From Javascript: in this case value cannot be returned because
    #    inter-process messaging is asynchronous, so must return value
    #    by calling js_callback.
    html = html.encode("utf-8", "replace")
    b64 = base64.b64encode(html).decode("utf-8", "replace")
    ret = "data:text/html;base64,{data}".format(data=b64)
    if js_callback:
        js_print(js_callback.GetFrame().GetBrowser(),
                 "Python", "html_to_data_uri",
                 "Called from Javascript. Will call Javascript callback now.")
        js_callback.Call(ret)
    else:
        return ret

def set_javascript_bindings(browser):
    external = External(browser)
    bindings = cef.JavascriptBindings(bindToFrames=False, bindToPopups=False)
    bindings.SetObject("external", external)
    browser.SetJavascriptBindings(bindings)

def js_print(browser, lang, event, msg):
    # Execute Javascript function "js_print"
    browser.ExecuteFunction("js_print", lang, event, msg)

class External(object):
    def __init__(self, browser):
        self.browser = browser

    def hello(_, *args):
        print(args)

    def put(_, *args):
        print(args)

    def test_multiple_callbacks(self, js_callback):
        """Test both javascript and python callbacks."""
        js_print(self.browser, "Python", "test_multiple_callbacks",
                 "Called from Javascript. Will call Javascript callback now.")

        def py_callback(msg_from_js):
            js_print(self.browser, "Python", "py_callback", msg_from_js)

        js_callback.Call("String sent from Python", py_callback)

def main():
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    # To change user agent use either "product_version"
    # or "user_agent" options. Explained in Tutorial in
    # "Change user agent string" section.
    settings = {
        # "product_version": "MyProduct/10.00",
        # "user_agent": "MyAgent/20.00 MyProduct/10.00",
    }
    cef.Initialize(settings=settings)
    browser = cef.CreateBrowserSync(url=html_to_data_uri(HTML_code),
                                    window_title="Tutorial")
    set_javascript_bindings(browser)
    cef.MessageLoop()
    cef.Shutdown()

if __name__ == '__main__':
    main()