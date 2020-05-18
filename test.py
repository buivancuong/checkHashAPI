import subprocess

cmd = './bf_client check 6d5b0d4b5b459ff3f68a58f3bfad3707'

result = subprocess.check_output(cmd, shell=True)

import re

nonexist = re.search('not.*', str(result))

if nonexist: print("nonexistant")
else: print("exist")