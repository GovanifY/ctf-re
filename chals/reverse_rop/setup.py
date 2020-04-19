import hashlib
import string
import random
import subprocess
import os
from pwn import *


def rng(index):
    BUF_SIZE = 65536 
    sha2 = hashlib.sha256()

    with open("flag.txt", 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha2.update(data)
    hash_final=bytes.fromhex(sha2.hexdigest())
    rng=hash_final[index]
    return rng

def write_line(fd, line, text):
    fdd = open(fd, "r")
    buf = fdd.readlines()
    buf.insert(line, text)
    
    fdd = open(fd, "w")
    fdd.writelines(buf) 
    fdd.close()

def replace_text(fd, to_change, text):
    fdd = open(fd, "r")
    buf = fdd.readlines()

    for i in range(0, len(buf)-1):
        buf[i]=buf[i].replace(to_change,text)

    fdd = open(fd, "w")
    fdd.writelines(buf) 
    fdd.close()

def replace_text_random_hash(fd, to_change):
    fdd = open(fd, "r")
    buf = fdd.readlines()

    for i in range(0, len(buf)-1):
        buf[i]=buf[i].replace(to_change,random_name(size=10, chars="0123456789abcdef"))

    fdd = open(fd, "w")
    fdd.writelines(buf) 
    fdd.close()



# deterministic seed to recreate files in a deterministic fashion
random.seed(rng(0)+(rng(3)<<1)+(rng(6)<<2)+(rng(8)<<3)+(rng(10)<<4)+(rng(1)<<5)+(rng(2)<<6))
# to avoid function redefinitions
def random_name(size=20, chars=string.ascii_uppercase + string.ascii_lowercase):
   return ''.join(random.choice(chars) for _ in range(size))

# maximum 32 
junk=["""
void FUNCTION_NAME (uint32_t v[2], uint32_t k[4]) {
    uint32_t v0=v[0], v1=v[1], sum=0, i;           /* set up */
    uint32_t delta=0x9E3779B9;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<32; i++) {                         /* basic cycle start */
        sum += delta;
        v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}
""",
"""
void FUNCTION_NAME (uint32_t v[2], uint32_t k[4]) {
    uint32_t v0=v[0], v1=v[1], sum=0xC6EF3720, i;  /* set up; sum is 32*delta */
    uint32_t delta=0x9E3779B9;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<32; i++) {                         /* basic cycle start */
        v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        sum -= delta;
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}
""",
"""
void *FUNCTION_NAME(void *block, size_t size) {
  void *new_block = malloc(size);
  if (new_block == NULL) return NULL;
  if (block != NULL) memcpy(new_block, block, size); // dirty but sound
  return new_block;
}
""",
"""
void * FUNCTION_NAME(size_t size) {
  void *block = malloc(size);
  if (block == NULL) {
    fprintf(stderr, "out of memory in static heap (%zd bytes requested)\n", size);
    abort();
  }
  return block;
}
""",
"""
unsigned int FUNCTION_NAME() {
    return (0x33&0xaaaaaaaa)>>1; // -> 0b101010... -> 1+3 aka mask odd numbers
}
""",
"""
uint16_t FUNCTION_NAME( uint8_t *data, int count )
{
   uint16_t sum1 = 0;
   uint16_t sum2 = 0;
   int index;

   for ( index = 0; index < count; ++index )
   {
      sum1 = (sum1 + data[index]) % 255;
      sum2 = (sum2 + sum1) % 255;
   }
   return (sum2 << 8) | sum1;
   }
""",
"""
int FUNCTION_NAME(int n)
{
    if (n <= 1)
        return n;
    return FUNCTION_NAME(n - 1) + FUNCTION_NAME(n - 2);
}
""",
"""
unsigned int FUNCTION_NAME(unsigned int b) {
    unsigned int a=b;
    unsigned int mod=a%b;
    while(mod>2){
        a=b;
        b=mod;
        mod=a%b;
    }
    if(mod==0)
        return b;
    return mod;
}
"""
]


# junk generator!!
line_junk=13
junk_count=rng(0)%len(junk)
for i in range(0, junk_count+1):
    junk_to_add=rng(i)%len(junk)
    # use this 
    name_call=random_name()
    write_line("main.c", line_junk, junk[junk_to_add].replace("FUNCTION_NAME",
        random_name()))


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

f = open("input", "wb")
f.write(exploit)
f.close()

subprocess.call(["strip", "reverse_rop"])


os.remove("main.c")
os.remove("Makefile")
os.remove("setup.py")
os.remove("flag.txt")

