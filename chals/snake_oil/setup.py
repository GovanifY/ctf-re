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

f = open("flag.txt", "r")
verif=[]
flag_enc=[]
flag=f.readline()
key=[rng(7), rng(9), rng(21), rng(12)]
i=0
for c in flag:
    flag_enc.append(ord(c)^key[(i%4)])
    verif.append(key[(i%4)])
    i+=1

s=bytes(flag_enc).hex()
flag_enc_c="\\x" + "\\x".join(a+b for a,b in zip(s[::2], s[1::2]))
s=bytes(verif).hex()
verif_c="\\x" + "\\x".join(a+b for a,b in zip(s[::2], s[1::2]))


replace_text("main.c", "VERIF_C", verif_c)
replace_text("main.c", "FLAG_ENC_C", flag_enc_c)

# junk code generation
write_junk_calls("main.c", 57, 4)
write_junk_calls("main.c", 50, 4)
write_junk_calls("main.c", 42, 4)
write_junk_calls("main.c", 34)
write_junk_body("main.c", 14)

subprocess.call("make", stdout=FNULL, stderr=FNULL)

# TESTING BINARY
try:
    output = subprocess.check_output("./snake_oil " + bytes(key).hex(), shell=True, stderr=subprocess.STDOUT)
except Exception as e:
    output = str(e.output)
if not flag.encode("utf-8") in output:
    fail_test()

os.remove("main.c")
os.remove("Makefile")
os.remove("setup.py")
os.remove("flag.txt")
