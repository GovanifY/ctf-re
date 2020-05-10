# in theory they can guess the 3 first chars of the key thanks to GY{ but they
# have to bruteforce the 4th
import subprocess
import os
import sys
from colorama import Fore, Back, Style
                    # chals_out/chal_name/team_name so 3
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from libchals import *
FNULL = open(os.devnull, 'w')

f = open("flag.txt", "r")
verif=[]
flag_enc=[]
flag=f.readline()
key=[rng(7), rng(9), rng(21), rng(12)]
i=0
for c in flag:
    flag_enc.append(ord(c)^(key[(i%4)]^rng(18)))
    i+=1
s=bytes(flag_enc).hex()
flag_enc_c="\\x" + "\\x".join(a+b for a,b in zip(s[::2], s[1::2]))

replace_text("main.c", "FLAG_ENC_C", flag_enc_c)
replace_text("main.c", "RANDOM_C", str(rng(18)))

# junk code generation
# we help a bit the rng since it is a reverse chal
set_junk_min(5)
write_junk_calls("main.c", 47, 4)
write_junk_calls("main.c", 41, 4)
write_junk_calls("main.c", 37, 4)
write_junk_calls("main.c", 33)
write_junk_body("main.c", 15)
subprocess.call("make", stdout=FNULL, stderr=FNULL)

f=open("input", "w")
f.write(bytes(key).hex())
f.close()
# TESTING BINARY
try:
    output = subprocess.check_output("./snake_oil_2 " + bytes(key).hex(), shell=True, stderr=subprocess.STDOUT)
except Exception as e:
    output = str(e.output)
if not flag.encode("utf-8") in output:
    fail_test()

os.remove("main.c")
os.remove("Makefile")
os.remove("setup.py")
os.remove("flag.txt")
os.remove("input")
