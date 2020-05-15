# from platforms.api import type_line
from recognition.actions.library import _keyboard as keyboard
import time
import os
import tempfile

def drop(num, mount_root='/mnt'):
    fd, temp_name = tempfile.mkstemp()
    read_name = f'{mount_root}/c' + temp_name.replace('\\', '/')[2:]
    keyboard.KeyPress.from_raw_text(f'ls > {read_name}').send()
    keyboard.KeyPress.from_space_delimited_string('enter').send()
    num = int(num)
    try:
        for i in range(200):
            if os.stat(temp_name).st_size > 0:
                with open(temp_name) as f:
                    for i, line in enumerate(f, start=1):
                        if i == num:
                            line = line.rstrip("\n")
                            keyboard.KeyPress.from_raw_text(f'cd "{line}"').send()
                            keyboard.KeyPress.from_space_delimited_string('enter').send()
                            break
                break
            time.sleep(0.01)
    finally:
        if os.path.isfile(temp_name):
            os.close(fd)
            os.remove(temp_name)