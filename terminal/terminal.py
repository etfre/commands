from platforms.api import type_line
import time
import os
import tempfile

def drop(num):
    num = int(num)
    _, temp_name = tempfile.mkstemp()
    read_name = '/mnt/c' + temp_name.replace('\\', '/')[2:]
    results = type_line([f'ls > {read_name}', ['enter']])
    time.sleep(.5)
    try:
        with open(temp_name) as f:
            for i, line in enumerate(f, start=1):
                if i == num:
                    line = line.rstrip("\n")
                    type_line([f'cd {line}', ['enter']])
                    break
    finally:
        if os.path.isfile(temp_name):
            os.remove(temp_name)