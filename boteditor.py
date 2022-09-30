import sys
import time
import binascii

import tb as traceback
import javascript

from browser import document as doc, window, alert, bind, html
from browser.html import DIV
from browser.widgets import dialog


has_ace = True


# from ai import robot



wrap_code = """

robot = None
listening = None
detected = None 

{}


robot.detected = detected
robot.listening = listening
# robot.ears(True)
# robot.eyes(True)
"""
def run(*args):
    global output
    doc["console"].value = ''
    
    src = editor.getValue()
    if storage is not None:
       storage["py_src"] = src

    t0 = time.perf_counter()
    try:
        ns = {'__name__':'__main__'}

        src = wrap_code.format(src)

        exec(src, ns)
        state = 1
    except Exception as exc:
        # traceback.print_exc(file=sys.stderr)
        state = 0
    sys.stdout.flush()
    output = doc["console"].value

    return state

try:
    editor = window.ace.edit("editor")
    editor.setTheme("ace/theme/cobalt")
    editor.session.setMode("ace/mode/python")
    editor.focus()

    def stop(event, *args):
        event.stop()
    
    editor.setOptions({
        'enableLiveAutocompletion': False,
        'highlightActiveLine': False,
        'highlightSelectedWord': True,
        'fontSize': '14px',
    })
    
    def foo(*args): 
        pass

    # editor.commands.addCommand({
    #     'name': "breakTheEditor", 
    #     'bindKey': "ctrl-c|ctrl-v|ctrl-x|ctrl-shift-v|shift-del|cmd-c|cmd-v|cmd-x", 
    #     'exec': foo
    # })

    editor.commands.addCommand({
        'name': "runCommand", 
        'bindKey': "ctrl-enter|cmd-enter", 
        'exec': run
    })

except:
    from browser import html
    editor = html.TEXTAREA(rows=20, cols=70)
    doc["editor"] <= editor
    def get_value(): return editor.value
    def set_value(x): editor.value = x
    editor.getValue = get_value
    editor.setValue = set_value
    has_ace = False

if hasattr(window, 'localStorage'):
    from browser.local_storage import storage
else:
    storage = None

def reset_src():
    if "code" in doc.query:
        code = doc.query.getlist("code")[0]
        editor.setValue(code)
    else:
        if storage is not None and "py_src" in storage:
            editor.setValue(storage["py_src"])
        else:
            editor.setValue('')
    editor.scrollToRow(0)
    editor.gotoLine(0)

def reset_src_area():
    if storage and "py_src" in storage:
        editor.value = storage["py_src"]
    else:
        editor.value = ''


class cOutput:
    encoding = 'utf-8'

    def __init__(self):
        self.cons = doc["console"]
        self.buf = ''

    def write(self, data):
        self.buf += str(data)

    def flush(self):
        self.cons.value += self.buf
        self.buf = ''

    def __len__(self):
        return len(self.buf)

if "console" in doc:
    cOut = cOutput()
    sys.stdout = cOut
    sys.stderr = cOut


def to_str(xx):
    return str(xx)

output = ''
doc["console"].value = '..'

# load a Python script
def load_script(evt):
    _name = evt.target.value + '?foo=%s' % time.time()
    editor.setValue(open(_name).read())



def share_code(ev):
    src = editor.getValue()
    
    if len(src) > 2048:
        alert('코드 길이는 2048자 이내로 작성해 주세요.')
    else:
        href = window.location.href.rsplit("?", 1)[0]
        query = doc.query
        query["code"] = src

        url = f"{href}{query}"
        alert(url)
        url = url.replace("(", "%28").replace(")", "%29")

        
        area = html.INPUT()
        area.style.top='0'
        area.style.height='0px'
        area.style.position='absolute'
        doc <= area
        area.value = url
        
        # copy to clipboard
        area.focus()
        area.select()
        doc.execCommand("copy")
        area.remove()
        editor.focus()
        alert('공유 링크가 [클립보드]에 복사되었습니다. (ctrl+v)')

if has_ace:
    reset_src()
else:
    reset_src_area()
