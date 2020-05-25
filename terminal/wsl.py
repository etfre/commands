from recognition.actions.library import _keyboard as keyboard, window, clipboard
import urllib.parse
import time
import os
import tempfile

MOUNT_ROOT = '/mnt'

def log_dir():
    tdir = os.path.join(tempfile.gettempdir(), 'osspeak_std')
    try:
        os.mkdir(tdir)
    except FileExistsError:
        pass
    return tdir

def linux_path(win_path):
    win_path_end = win_path.replace(os.sep, '/')[2:]
    return f'{MOUNT_ROOT}/c{win_path_end}'

def new_logfile_path():
    return os.path.join(log_dir(), 'osspeak_log.txt')

def navigate_list(gather_cmd, exec_cmd, num, modify_line=None):
    fd, temp_name = tempfile.mkstemp()
    read_name = linux_path(temp_name)
    keyboard.KeyPress.from_raw_text(f'{gather_cmd} > {read_name}').send()
    keyboard.KeyPress.from_space_delimited_string('enter').send()
    num = int(num)
    try:
        for i in range(200):
            if os.stat(temp_name).st_size > 0:
                with open(temp_name) as f:
                    for i, line in enumerate(f, start=1):
                        if i == num:
                            line = line.rstrip("\n")
                            if modify_line:
                                line = modify_line(line)
                            if isinstance(exec_cmd, str):
                                keyboard.KeyPress.from_raw_text(f'{exec_cmd} "{line}"').send()
                                keyboard.KeyPress.from_space_delimited_string('enter').send()
                                break
                            else:
                                return exec_cmd(line)
                break
            time.sleep(0.01)
    finally:
        if os.path.isfile(temp_name):
            os.close(fd)
            os.remove(temp_name)

def checkout_numbered_branch(num):
    def modify_line(line):
        if line.startswith('*'):
            line = line[1:]
        return line.lstrip()
    return navigate_list('git branch', 'git checkout', num, modify_line=modify_line)

def list_files_to_clipboard(num):
    
    def exec_cmd(line):
        clipboard.set(line)
    return navigate_list('ls', exec_cmd, num)

def drop(num):
    return navigate_list('ls', 'cd', num)
    
def to_clipboard():
    def exec_cmd(line):
        clipboard.set(line)
    return navigate_list('', exec_cmd, 1)
    
def run_and_log(s):
    path = linux_path(new_logfile_path())
    keyboard.KeyPress.from_raw_text(f'{s}|& tee {path}').send()
    keyboard.KeyPress.from_space_delimited_string('enter').send()

def log_stderr():
    path = linux_path(new_logfile_path())
    keyboard.KeyPress.from_raw_text(f'|& tee {path}').send()

def last_modified_file():
    dir_path = log_dir()
    files = os.listdir(dir_path)
    paths = [os.path.join(dir_path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

def read_logfile(name, lines):
    if lines is None:
        with open(name) as f:
            return f.read()
    with open(name, 'rb') as f:
        return tail(f, lines)

def tail(f, lines):
    total_lines_wanted = lines
    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = []
    while lines_to_go > 0 and block_end_byte > 0:
        if block_end_byte - BLOCK_SIZE > 0:
            f.seek(block_number * BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            f.seek(0, 0)
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count(b'\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = b''.join(reversed(blocks))
    return b'\n'.join(all_read_text.splitlines()[-total_lines_wanted:]).decode('utf8')

def search(file_name=None, lines=None):
    if file_name is None:
        file_name = last_modified_file()
    else:
        file_name = os.path.join(log_dir(), file_name)
    file_text = read_logfile(file_name, lines)
    formatted_text = ' '.join(file_text.split('\n'))
    qparams = urllib.parse.urlencode({'q': formatted_text})
    window.focus('google chrome')
    window.wait('google chrome', timeout=5, raise_on_timeout=True)
    keyboard.KeyPress.from_space_delimited_string('ctrl l').send()
    time.sleep(0.2)
    url = f'https://google.com/search?{qparams}'
    keyboard.KeyPress.from_raw_text(url).send()
    keyboard.KeyPress.from_space_delimited_string('enter').send()