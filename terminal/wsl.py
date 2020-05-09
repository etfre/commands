# from platforms.api import type_line
from recognition.actions.library import _keyboard as keyboard
import time
import os
import tempfile

def drop(num):
    num = int(num)
    _, temp_name = tempfile.mkstemp()
    read_name = '/mnt/c' + temp_name.replace('\\', '/')[2:]
    keyboard.KeyPress.from_raw_text(f'ls > {read_name}').send()
    keyboard.KeyPress.from_space_delimited_string('enter').send()
    time.sleep(.5)
    try:
        with open(temp_name) as f:
            for i, line in enumerate(f, start=1):
                if i == num:
                    line = line.rstrip("\n")
                    keyboard.KeyPress.from_raw_text(f'cd {line}').send()
                    keyboard.KeyPress.from_space_delimited_string('enter').send()
                    break
    finally:
        if os.path.isfile(temp_name):
            os.remove(temp_name)