import time
import threading
from recognition.actions.library import _mouse as mouse

# DIREC
KILL_EVENTS = set()

def _run_scan(kill_event, x, y):
    mouse.press()
    while not kill_event.is_set():
        mouse.move_relative(x=x, y=y)
        time.sleep(0.05)
    KILL_EVENTS.remove(kill_event)
    print('end run scan')

def scan(x=0, y=0):
    stop()
    kill_event = threading.Event()
    KILL_EVENTS.add(kill_event)
    threading.Thread(target=_run_scan, args=(kill_event, int(x), int(y))).start()
    print('end scan call')

def stop():
    for evt in KILL_EVENTS:
        evt.set()
    mouse.release()
