import subprocess
import os
import sys
from colorama import Fore, Back, Style
                    # chals_out/chal_name/team_name so 3
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from libchals import *

from pwn import *

context.log_level = 'error'
FNULL = open(os.devnull, 'w')


# junk code generation
write_junk_calls("main.c", 53, 3)
write_junk_calls("main.c", 23, 3)
write_junk_calls("main.c", 19)
write_junk_body("main.c", 14)

# replace flags in source file
f = open("flag.txt", "r")
flag=f.readline()
flag1=flag[:30]
flag2=flag[30:60]  
flag3=flag[60:] 
replace_text("main.c", "FLAG_PART_1", flag1)
replace_text("main.c", "FLAG_PART_2", flag2)
replace_text("main.c", "FLAG_PART_3", flag3)
replace_text_random_hash("main.c", "FLAG_WRONG", 30)

subprocess.call("make", stdout=FNULL, stderr=FNULL)

os.remove("main.c")
os.remove("Makefile")
os.remove("setup.py")
os.remove("flag.txt")
