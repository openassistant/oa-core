from core import command_registry, oa

from abilities.interact import say, play, mind


kws = {}
command = command_registry(kws)

@command("boot mind")
def response_sound():
  play('r2d2.wav')

@command("open assistant")
def open_root():
  play('beep_open.wav')
  mind('root')

@command(["list commands", "help"])
def list_commands():
    say('The currently available voice commands are..')
    [say(cmd) for cmd in kws.keys()]

@command("stop listening")
def do_exit():
    oa.core.finished.set()