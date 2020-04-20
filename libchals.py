import random 
import hashlib
import string
from colorama import Fore, Back, Style
from pathlib import Path

"""
Some limitations:
    The junk code must be added at the beginning of the source file
    You must write junk code from bottom to top, aka first junk calls,
    then junk definition, from the bottom up.
"""
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

def fail_test():
    print(Fore.RED + "ERROR: BINARY IN " + str(Path().absolute()) + " IS NOT SOLVABLE")
    print(Style.RESET_ALL)



# deterministic seed to recreate files in a deterministic fashion
random.seed(rng(0)+(rng(3)<<1)+(rng(6)<<2)+(rng(8)<<3)+(rng(10)<<4)+(rng(1)<<5)+(rng(2)<<6))
# to avoid function redefinitions
def random_name(size=20, chars=string.ascii_uppercase + string.ascii_lowercase):
   return ''.join(random.choice(chars) for _ in range(size))

junk=["""
typedef struct {
    char infos[50];
    uint8_t cle[16];
}FUNCTION_NAMEstru;

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
typedef struct {
    char infos[50];
    uint8_t cle[16];
}FUNCTION_NAMEstru;

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
    fprintf(stderr, "out of memory in static heap cannot calculate flag");
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

junk_calls=[
"""
FUNCTION_NAMEstru VAR_NAME;
memset(VAR_NAME.infos, 0xCCFF, sizeof(VAR_NAME.infos));
memset(VAR_NAME.cle, 0xAABB, sizeof(VAR_NAME.cle));
for(int VAR_NAMEb=0; VAR_NAMEb<50; VAR_NAMEb+=4) {
    FUNCTION_NAME((uint32_t*)(VAR_NAME.infos+VAR_NAMEb), (uint32_t*)VAR_NAME.cle);
}
""",
"""
FUNCTION_NAMEstru VAR_NAME;
memset(VAR_NAME.infos, 0xAABB, sizeof(VAR_NAME.infos));
memset(VAR_NAME.cle, 0xCCFF, sizeof(VAR_NAME.cle));
for(int VAR_NAMEb=0; VAR_NAMEb<50; VAR_NAMEb+=4) {
    FUNCTION_NAME((uint32_t*)(VAR_NAME.infos+VAR_NAMEb), (uint32_t*)VAR_NAME.cle);
}
""",
"""
/* This is left intentionally blank */
""",
"""
int32_t *VAR_NAME = FUNCTION_NAME(0x17 * sizeof(int32_t));
char VAR_NAMEb [50];
if (VAR_NAME == NULL) /* Memory allocation fails */
{
sprintf (VAR_NAMEb, "Couldn't");
}
else  /* Memory allocation successful */
{
sprintf (VAR_NAMEb, "successful");
}
""",
"""
for(unsigned int VAR_NAME=0; VAR_NAME<15; VAR_NAME--){
    VAR_NAME=FUNCTION_NAME();
}
""",
"""
uint8_t VAR_NAME[120];
VAR_NAME[0]=0x3;
VAR_NAME[1]=0xD3;
VAR_NAME[2]=0x3E33;
VAR_NAME[3]=0x394EDDE;
VAR_NAME[4]=0xAAAA1;
VAR_NAME[5]=0xFFFFFFFF;
uint16_t VAR_NAMEa= FUNCTION_NAME(VAR_NAME, 6);
char VAR_NAMEb [50];
sprintf (VAR_NAMEb, "result: %d", VAR_NAMEa);
""",
"""
int VAR_NAME=FUNCTION_NAME(FUNCTION_NAME(3));
VAR_NAME=VAR_NAME<<3;
""",
"""
unsigned int VAR_NAME=FUNCTION_NAME(157);
VAR_NAME=VAR_NAME+VAR_NAME;
VAR_NAME=(VAR_NAME/VAR_NAME)*2;
"""
]

fun_names=[]
junk_called=0
def write_junk_body(fd, line):
    # junk generator!!
    dont_gen_name=False
    junk_count=rng(0)%len(junk)
    if(fun_names!=[]):
        dont_gen_name=True
    for i in range(0, junk_count+1):
        junk_to_add=rng(i%len(junk))%len(junk)
        # use this 
        if(not dont_gen_name):
            fun_names.append(random_name())
        write_line(fd, line,
                junk[junk_to_add].replace("FUNCTION_NAME",fun_names[i]))

def write_junk_calls(fd, line, count=-1):
    # junk generator!!
    global junk_called
    junk_count=rng(0)%len(junk)
    if(count==-1):
        count=junk_count+1
    else:
        count=junk_called + junk_count//count
    if(fun_names==[] and junk_called==0):
        gen_fun_names()
    for i in range(junk_called, count):
        junk_to_add=rng(i%len(junk))%len(junk)
        # use this 
        tmp=junk_calls[junk_to_add].replace("FUNCTION_NAME", fun_names[i])
        write_line(fd, line, tmp.replace("VAR_NAME", random_name()))
        junk_called+=1

def gen_fun_names():
    # junk generator!!
    junk_count=rng(0)%len(junk)
    for i in range(0, junk_count+1):
        junk_to_add=rng(i%len(junk))%len(junk)
        # use this 
        fun_names.append(random_name())
