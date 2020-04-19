import os
import json
import pathlib
import hashlib
import errno
import shutil
import subprocess

rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))


ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def small_hash(name):
    checksum=0
    for byte in name:
        # get last bit of checksum
        b=checksum & 0b11111111
        # addition on 8bits
        b+=ord(byte)
        b&= 0b11111111
        #clear last bits of checksum
        checksum = checksum & 0b11111111111111111111111100000000
        # checksum last 8 bits = b
        checksum = checksum | b
        # rol checksum
        checksum=rol(checksum, 3, 32)

    return checksum.to_bytes(4, byteorder='big')
 
def copy_dir(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

team_count=0
teams={}
submissions=[]
chals=[]
for i in next(os.walk('chals'))[1]:
    chals.append(i)

with open("teams.json", "r") as read_file:
    data = json.load(read_file)
    team_count=data['count']
    for i in range(0, team_count):
        teams[data['results'][i]['id']] = data['results'][i]['name']

with open("submissions.json", "r") as read_file:
    data = json.load(read_file)
    sub_count=data['count']
    for i in range(0, sub_count):
        submissions.append([data['results'][i]['provided'],
            data['results'][i]['team_id']])

for i in submissions:
    print("%s was submitted by %s" % (i[0], teams[i[1]]))

exit()

# flag creation is a bit complex: in theory we do a sha2 for each challenge
# name, but also calculate through a custom hash team name + chal name that we
# add inside this flag at random bytes for each chal
for i in chals:
    regex_done=False

    # we calculate the location of the identifying bytes
    salt_chal=small_hash(i)
    salts=[]
    for z in range(0, 4):
        salts.append(salt_chal[z]%32)
        if(salts[z]==0):
            salts[z]+=2
        elif(z==32):
            salts[z]-=2

    for y in team_names:
        copy_dir("chals/" + i, "chals_out/" + i + "/" +  y)
        uni_hash=small_hash(i+y)
        # make it a bit harder to guess the format of the sha2
        chal_name=i+"1378528"
        hash_final=bytearray(bytes.fromhex(hashlib.sha256(chal_name.encode()).hexdigest()))
        # we replace by the identifying bytes
        hash_final[salts[0]]=uni_hash[0]
        hash_final[salts[1]]=uni_hash[1]
        hash_final[salts[2]]=uni_hash[2]
        hash_final[salts[3]]=uni_hash[3]
        hash_final_str=hash_final.hex()
        flag = "GY{" + hash_final_str + "}"
        with open("chals_out/" + i + "/" + y + "/flag.txt", "w") as fdflag:
                fdflag.write(flag)

        # generate the challenge
        subprocess.call(["python3", "setup.py"], cwd="chals_out/" + i + "/" + y)

        if(regex_done==False): 
            regex = list(flag)
            # we want a global regex for all challengers, so we replace
            # identifying bytes in the regex. The anti cheat script is going to
            # be ran after the ctf anyways
            regex[((salts[0]*2)+3)]="."
            regex[((salts[0]*2)+3)+1]="."

            regex[((salts[1]*2)+3)]="."
            regex[((salts[1]*2)+3)+1]="."

            regex[((salts[2]*2)+3)]="."
            regex[((salts[2]*2)+3)+1]="."

            regex[((salts[3]*2)+3)]="."
            regex[((salts[3]*2)+3)+1]="."

            with open("chals_out/" + i + "/regex.txt", "w") as fdregex:
                fdregex.write(''.join(regex))
            regex_done=True




