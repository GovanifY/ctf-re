import subprocess
import os
import sys
import shutil
from colorama import Fore, Back, Style
                    # chals_out/chal_name/team_name so 3
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from libchals import *

FNULL = open(os.devnull, 'w')

# junk code generation
write_junk_calls("main.c", 64, 3)
write_junk_calls("main.c", 50, 3)
write_junk_body("main.c", 14)

subprocess.call("make", stdout=FNULL, stderr=FNULL)


# testing this binary is a pain because race condition and is unlikely to fail
# anyways, so we don't

os.remove("main.c")
os.remove("Makefile")
os.remove("setup.py")
shutil.rmtree("solution")
