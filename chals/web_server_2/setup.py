# just print whatever is on the stack and the flag magically appears, format
# string on file not found exceptions
import subprocess
import os
import sys
from colorama import Fore, Back, Style
                    # chals_out/chal_name/team_name so 3
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from libchals import *

FNULL = open(os.devnull, 'w')

# junk code generation
# we help a bit the rng since it is a reverse chal
write_junk_calls("main.c", 467, 6)
write_junk_calls("main.c", 401, 6)
write_junk_calls("main.c", 394, 6)
write_junk_calls("main.c", 333, 6)
write_junk_calls("main.c", 309, 6)
write_junk_calls("main.c", 198)
write_junk_body("main.c", 23)

subprocess.call("make", stdout=FNULL, stderr=FNULL)


# TESTING BINARY
# TODO: Test suite for web_server_2 

os.remove("main.c")
os.remove("Makefile")
os.remove("setup.py")
