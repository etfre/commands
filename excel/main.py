import sprecgrammars
import time
import json
import os
import subprocess
from common import proc
from user.settings import user_settings

VOICE_EXCEL = os.path.join(user_settings['external_directory'], 'voiceexcel')
VOICE_EXCEL_MAIN = os.path.join(VOICE_EXCEL, 'voiceexcel', 'main.py')

class ExcelProcessManager(proc.ProcessManager):

    def __init__(self):
        python_path = os.path.join(VOICE_EXCEL, 'scripts', 'python.exe')
        super().__init__([python_path, VOICE_EXCEL_MAIN], on_message=self.on_message)
        # super().__init__(['python ' + VOICE_EXCEL_MAIN], on_message=self.on_message)

    def on_message(self, msg):
        print('got ' + msg)

    def send_message(self, name, *a, **k):
        msg = {
            'name': name,
            'args': a,
            'kwargs': k,
        }
        super().send_message(json.dumps(msg))

def message(name, *a, **k):
    excel.send_message(name, *a, **k)

excel = ExcelProcessManager()
print('excel extension activated')