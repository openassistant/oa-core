from core import command_registry
from abilities.core import mind, play

kws = {}

command = command_registry(kws)

@command("boot mind")
def response_sound():
  play('r2d2.wav')

@command("open assistant")
def open_root():
  play('beep_open.wav')
  mind('root')
